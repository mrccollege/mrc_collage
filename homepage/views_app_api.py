import uuid
import requests
import json
from datetime import datetime, timedelta
from django.db import connection

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserProfile
from courses.models import Course, CoursePurchased, MonthMoney, CourseMaster, CourseMasterDisplay
from homepage.models import CouponCode, HomepageTopMedia, FeedbackImage


def generate_tran_id():
    return "TID" + str(uuid.uuid4().hex[:12])


def calculate_future_date(month):
    return datetime.now() + timedelta(days=30 * int(month))


def get_phonepe_config():
    return {
        "client_id": getattr(settings, "PHONEPE_CLIENT_ID", getattr(settings, "PHONEPE_MERCHANT_ID", "")),
        "client_secret": getattr(settings, "PHONEPE_CLIENT_SECRET", getattr(settings, "PHONEPE_SALT_KEY", "")),
        "client_version": int(getattr(settings, "PHONEPE_CLIENT_VERSION", 1)),
        "merchant_id": getattr(settings, "PHONEPE_MERCHANT_ID", ""),
        "environment": getattr(settings, "PHONEPE_ENVIRONMENT", "PRODUCTION"),
    }


def get_phonepe_access_token():
    phonepe_config = get_phonepe_config()
    url = "https://api.phonepe.com/apis/identity-manager/v1/oauth/token"
    payload = {
        "client_version": phonepe_config["client_version"],
        "grant_type": "client_credentials",
        "client_id": phonepe_config["client_id"],
        "client_secret": phonepe_config["client_secret"],
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("access_token")


def resolve_checkout_amount(course_id, month, apply_coupon):
    discount = 0
    course_price = MonthMoney.objects.filter(course_id=course_id, month=month)
    if course_price:
        base_price = course_price[0].money
    else:
        course_price = MonthMoney.objects.filter(course_id=course_id).first()
        if not course_price:
            raise Exception("Pricing not found")
        base_price = course_price.money
        month = course_price.month

    if apply_coupon:
        is_exist = CouponCode.objects.filter(coupon_code__exact=apply_coupon)
        if is_exist:
            discount = is_exist[0].percent
            after_discount = discount * base_price / 100
            course_price = base_price - after_discount
        else:
            course_price = base_price
    else:
        course_price = base_price

    return int(course_price), int(discount), month


def create_phonepe_checkout(user_id, course_id, month, apply_coupon, redirect_url, merchant_reference_id=None):
    course_price, discount, resolved_month = resolve_checkout_amount(course_id, month, apply_coupon)
    access_token = get_phonepe_access_token()
    merchant_reference_id = merchant_reference_id or generate_tran_id()
    final_payload = {
        "merchantOrderId": merchant_reference_id,
        "amount": course_price * 100,
        "expireAfter": 1200,
        "metaInfo": {
            "udf1": str(user_id),
            "udf2": str(course_id),
            "udf3": str(resolved_month),
            "udf4": apply_coupon or "",
            "udf5": "therapy-app"
        },
        "paymentFlow": {
            "type": "PG_CHECKOUT",
            "message": "Payment message used for collect requests",
            "merchantUrls": {
                "redirectUrl": redirect_url
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"O-Bearer {access_token}"
    }

    response = requests.post(
        "https://api.phonepe.com/apis/pg/checkout/v2/pay",
        headers=headers,
        json=final_payload,
        timeout=30,
    )
    response.raise_for_status()
    response_data = response.json()
    return response_data, access_token, merchant_reference_id, course_price, discount, resolved_month


def persist_course_payment(user_id, course_id, order_id, access_token, merchant_reference_id, course_price, discount,
                           month, apply_coupon=''):
    future_date = calculate_future_date(int(month))
    same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
    update_payload = {
        "razorpay_order_id": order_id,
        "merchant_reference_id": merchant_reference_id,
        "access_token": access_token,
        "price": course_price,
        "totalprice": course_price,
        "discount": discount,
        "coupon_code": apply_coupon or "",
        "month": month,
        "start_date": datetime.now(),
        "end_date": future_date,
        "payment_status": "pending",
    }

    if same_user:
        same_user.update(**update_payload)
    else:
        CoursePurchased.objects.create(
            user_id=user_id,
            course_id=course_id,
            **update_payload,
        )


@csrf_exempt
def app_get_service_month(request):
    if request.method != "GET":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    course_id = request.GET.get("course_id")
    if not course_id:
        return JsonResponse({"status": "failed", "msg": "course_id is required"}, status=400)

    price_data = MonthMoney.objects.filter(course_id=course_id).order_by("month")
    data_list = []
    for item in price_data:
        data_list.append({
            "id": item.id,
            "month": item.month,
            "price": item.money,
        })

    return JsonResponse({"status": "success", "data": data_list})


@csrf_exempt
def app_get_service_price(request):
    if request.method != "GET":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    user_id = request.session.get("user_id") or request.GET.get("user_id")
    course_id = request.GET.get("course_id")
    month_id = request.GET.get("month_id")

    if not user_id or not course_id or not month_id:
        return JsonResponse({"status": "failed", "msg": "user_id, course_id and month_id are required"}, status=400)

    try:
        price_data = MonthMoney.objects.get(id=month_id)
    except MonthMoney.DoesNotExist:
        return JsonResponse({"status": "failed", "msg": "Pricing row not found"}, status=404)

    data_dict = {
        "month": price_data.month,
        "price": price_data.money,
    }

    future_date = calculate_future_date(data_dict["month"])
    same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)

    if same_user:
        same_user.update(
            price=data_dict["price"],
            totalprice=data_dict["price"],
            month=data_dict["month"],
            start_date=datetime.now(),
            end_date=future_date,
        )
    else:
        CoursePurchased.objects.create(
            user_id=user_id,
            course_id=course_id,
            price=data_dict["price"],
            totalprice=data_dict["price"],
            month=data_dict["month"],
            end_date=future_date,
        )

    return JsonResponse({
        "status": "success",
        "data": data_dict,
        "course_id": course_id,
    })


@csrf_exempt
def app_apply_coupon_code(request):
    if request.method != "GET":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    user_id = request.session.get("user_id") or request.GET.get("user_id")
    course_id = request.GET.get("course_id")
    coupon_code = request.GET.get("coupon_code")

    if not user_id or not course_id:
        return JsonResponse({"status": "failed", "msg": "user_id and course_id are required"}, status=400)

    coupon_data = CouponCode.objects.filter(coupon_code__exact=coupon_code)
    coupon_dict = {}
    if coupon_data:
        coupon_dict["percent"] = coupon_data[0].percent
        coupon_dict["coupon_code"] = coupon_data[0].coupon_code

    same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
    if same_user:
        try:
            same_user.update(
                discount=coupon_dict.get("percent", 0),
                coupon_code=coupon_dict.get("coupon_code", ""),
                start_date=datetime.now(),
            )
        except Exception:
            same_user.update(
                discount=0,
                coupon_code="",
                start_date=datetime.now(),
            )

    return JsonResponse({
        "status": "success",
        "coupon_data": coupon_dict
    })


@csrf_exempt
def app_buy_course_detail(request, course_id):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    user_id = request.session.get("user_id") or request.POST.get("user_id")
    month = request.POST.get("month")
    apply_coupon = request.POST.get("apply_coupon") or request.POST.get("coupon_code")

    if not user_id:
        return JsonResponse({"status": "failed", "msg": "user_id is required"}, status=400)

    try:
        merchant_reference_id = generate_tran_id()
        response_data, access_token, merchant_reference_id, course_price, discount, resolved_month = create_phonepe_checkout(
            user_id=user_id,
            course_id=course_id,
            month=month,
            apply_coupon=apply_coupon,
            redirect_url=f"https://mrctherapy.com/app-payment-return/{merchant_reference_id}/",
            merchant_reference_id=merchant_reference_id,
        )

        # PhonePe nests everything inside response_data["data"]["instrumentResponse"]
        data_dict = response_data.get("data", {})
        order_id = response_data.get("orderId") or data_dict.get("orderId") or merchant_reference_id

        # Extract redirect URL from instrumentResponse → redirectInfo → url
        instrument_response = data_dict.get("instrumentResponse", {})
        redirect_info = instrument_response.get("redirectInfo", {})
        redirect_url = (
            redirect_info.get("url")
            or data_dict.get("redirectUrl")
            or response_data.get("redirectUrl", "")
        )

        # Extract QR / UPI string so the mobile app can render a scannable QR code
        qr_string = (
            instrument_response.get("qrData")
            or instrument_response.get("qrString")
            or instrument_response.get("intentUrl")
            or ""
        )

        persist_course_payment(
            user_id=user_id,
            course_id=course_id,
            order_id=order_id,
            access_token=access_token,
            merchant_reference_id=merchant_reference_id,
            course_price=course_price,
            discount=discount,
            month=resolved_month,
            apply_coupon=apply_coupon,
        )

        return JsonResponse({
            "status": "success",
            "redirectUrl": redirect_url,
            "qrString": qr_string,
            "orderId": order_id,
            "merchant_reference_id": merchant_reference_id,
            "amount": course_price,
            "discount": discount,
            "month": resolved_month,
            "raw": response_data,
        })
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": str(e)}, status=500)


def get_order_status(merchant_order_id, details=False, error_context=False):
    cp = CoursePurchased.objects.filter(merchant_reference_id=merchant_order_id).first()
    if not cp:
        return {"error": "Invalid merchant order id"}

    url = f"https://api.phonepe.com/apis/pg/checkout/v2/order/{merchant_order_id}/status"
    params = {
        "details": str(details).lower(),
        "errorContext": str(error_context).lower(),
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"O-Bearer {cp.access_token}",
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        status = data.get("state")
        if status == "COMPLETED":
            CoursePurchased.objects.filter(merchant_reference_id=merchant_order_id).update(payment_status="success")
        elif status in ["FAILED", "EXPIRED"]:
            CoursePurchased.objects.filter(merchant_reference_id=merchant_order_id).update(payment_status="failed")
        return data
    except Exception as e:
        return {"error": str(e)}


@csrf_exempt
def app_payment_status(request):
    if request.method != "GET":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    merchant_reference_id = request.GET.get("merchant_reference_id")
    if not merchant_reference_id:
        return JsonResponse({"status": "failed", "msg": "merchant_reference_id is required"}, status=400)

    response = get_order_status(merchant_reference_id, details=True, error_context=True)
    if response.get("error"):
        return JsonResponse({"status": "failed", "msg": response["error"]}, status=500)

    return JsonResponse({
        "status": "success",
        "payment_state": response.get("state", "PENDING"),
        "phonepe_response": response,
    })


@csrf_exempt
def app_payment_confirm(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    merchant_reference_id = request.POST.get("merchant_reference_id")
    if not merchant_reference_id:
        return JsonResponse({"status": "failed", "msg": "merchant_reference_id is required"}, status=400)

    cp = CoursePurchased.objects.filter(merchant_reference_id=merchant_reference_id).first()
    if not cp:
        return JsonResponse({"status": "failed", "msg": "Invalid merchant_reference_id"}, status=404)

    if cp.payment_status not in ["success", "renew"]:
        return JsonResponse({
            "status": "failed",
            "msg": "Payment not completed yet",
            "payment_status": cp.payment_status,
        }, status=400)

    profile = UserProfile.objects.filter(user_id=cp.user_id).first()

    return JsonResponse({
        "status": "success",
        "msg": "Enrollment confirmed",
        "course_id": cp.course_id,
        "user_id": cp.user_id,
        "payment_status": cp.payment_status,
        "phone": profile.mobile if profile and profile.mobile else "",
    })


@csrf_exempt
def app_payment_return(request, merchant_reference_id):
    return HttpResponse(f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <title>Returning to App</title>
        <script>
          window.onload = function() {{
            window.location.href = "therapyapp://payment-return";
            setTimeout(function() {{
              window.location.href = "https://mrctherapy.com/";
            }}, 1500);
          }};
        </script>
      </head>
      <body style="font-family: Arial, sans-serif; text-align:center; padding:40px;">
        <h2>Returning to app...</h2>
        <p>If the app does not open, <a href="therapyapp://payment-return">tap here</a>.</p>
        <p>Reference: {merchant_reference_id}</p>
      </body>
    </html>
    """)


@csrf_exempt
def app_home_top_media(request):
    if request.method == "GET":
        rows = HomepageTopMedia.objects.select_related("course").order_by("sort_order", "id")
        data = []

        for item in rows:
            data.append({
                "id": item.id,
                "url": item.url or "",
                "course_id": item.course_id,
                "course_name": item.course.name if item.course else "",
                "course_image": request.build_absolute_uri(item.course.course_image.url)
                if item.course and item.course.course_image
                else "",
                "sort_order": item.sort_order,
            })

        return JsonResponse({"status": "success", "data": data})

    if request.method == "POST":
        body = {}
        try:
            if request.body:
                body = json.loads(request.body.decode("utf-8"))
        except Exception:
            body = {}

        row_id = body.get("id") or request.POST.get("id")
        url = (body.get("url") or request.POST.get("url") or "").strip()
        course_id = body.get("course_id") or request.POST.get("course_id")
        sort_order = body.get("sort_order") or request.POST.get("sort_order") or 0

        if not course_id:
            return JsonResponse({"status": "failed", "msg": "course_id is required"}, status=400)

        try:
            course = Course.objects.get(id=int(course_id))
        except (Course.DoesNotExist, TypeError, ValueError):
            return JsonResponse({"status": "failed", "msg": "Invalid course_id"}, status=404)

        try:
            sort_order = int(sort_order)
        except Exception:
            sort_order = 0

        if row_id:
            try:
                obj = HomepageTopMedia.objects.get(id=row_id)
            except HomepageTopMedia.DoesNotExist:
                return JsonResponse({"status": "failed", "msg": "Invalid id"}, status=404)

            obj.url = url
            obj.course = course
            obj.sort_order = sort_order
            obj.save()
            message = "Row updated successfully"
        else:
            obj = HomepageTopMedia.objects.create(
                url=url,
                course=course,
                sort_order=sort_order,
            )
            message = "Row created successfully"

        return JsonResponse({
            "status": "success",
            "msg": message,
            "data": {
                "id": obj.id,
                "url": obj.url or "",
                "course_id": obj.course_id,
                "course_name": obj.course.name if obj.course else "",
                "course_image": request.build_absolute_uri(obj.course.course_image.url)
                if obj.course and obj.course.course_image
                else "",
                "sort_order": obj.sort_order,
            },
        })

    return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)



# ... existing code (generate_tran_id, app_buy_course_detail, etc.) ...

@csrf_exempt
def app_upload_feedback_image(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    title = request.POST.get("title", "").strip()
    image_file = request.FILES.get("image")

    if not image_file:
        return JsonResponse({"status": "failed", "msg": "No image file provided"}, status=400)

    try:
        feedback_image = FeedbackImage.objects.create(
            title=title,
            image=image_file
        )
        return JsonResponse({
            "status": "success",
            "msg": "Image uploaded successfully",
            "data": {
                "id": feedback_image.id,
                "title": feedback_image.title,
                "image_url": request.build_absolute_uri(feedback_image.image.url)
            }
        })
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": str(e)}, status=500)

# ... (existing FeedbackImage upload view) ...

@csrf_exempt
def app_get_feedback_images(request):
    if request.method != "GET":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    images = FeedbackImage.objects.all().order_by("-id")
    data = []
    for img in images:
        data.append({
            "id": img.id,
            "title": img.title or "",
            "image_url": request.build_absolute_uri(img.image.url) if img.image else "",
            "created_at": img.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({"status": "success", "data": data})

@csrf_exempt
def app_delete_feedback_image(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    image_id = request.POST.get("id")
    if not image_id:
        return JsonResponse({"status": "failed", "msg": "id is required"}, status=400)

    try:
        feedback_image = FeedbackImage.objects.get(id=image_id)
        feedback_image.delete()
        return JsonResponse({"status": "success", "msg": "Image deleted successfully"})
    except FeedbackImage.DoesNotExist:
        return JsonResponse({"status": "failed", "msg": "Image not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": str(e)}, status=500)

@csrf_exempt
def app_edit_feedback_image(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    image_id = request.POST.get("id")
    title = request.POST.get("title")

    if not image_id:
        return JsonResponse({"status": "failed", "msg": "id is required"}, status=400)

    try:
        feedback_image = FeedbackImage.objects.get(id=image_id)
        if title is not None:
            feedback_image.title = title.strip()
        
        if request.FILES.get("image"):
            feedback_image.image = request.FILES.get("image")
            
        feedback_image.save()

        return JsonResponse({
            "status": "success",
            "msg": "Image updated successfully",
            "data": {
                "id": feedback_image.id,
                "title": feedback_image.title,
                "image_url": request.build_absolute_uri(feedback_image.image.url)
            }
        })
    except FeedbackImage.DoesNotExist:
        return JsonResponse({"status": "failed", "msg": "Image not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": str(e)}, status=500)


# to udate ranking
@csrf_exempt
def app_get_courses(request):
    try:
        all_courses = Course.objects.all().order_by('id')
        data = []

        with connection.cursor() as cursor:
            for c in all_courses:
                cursor.execute(
                    "SELECT screen_order, rating FROM courses_coursemasterdisplay WHERE course_master_id = %s",
                    [c.id]
                )
                row = cursor.fetchone()
                order, rating = (row[0], row[1]) if row else (0, 0.0)

                data.append({
                    "id": c.id,
                    "name": c.name or "Unnamed",
                    "screen_order": order,
                    "rating": rating,
                })

        return JsonResponse({"status": "success", "data": data})

    except Exception as e:
        return JsonResponse({"status": "failed", "msg": str(e)}, status=500)


@csrf_exempt
def update_master_bulk(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Only POST allowed"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        items = body.get("items", [])

        with connection.cursor() as cursor:
            for item in items:
                course_id = item.get("id")
                order = item.get("screen_order", 0)
                rating = item.get("rating", 0.0)

                if not course_id:
                    continue

                # check if record exists
                cursor.execute(
                    "SELECT id FROM courses_coursemasterdisplay WHERE course_master_id = %s",
                    [course_id]
                )

                if cursor.fetchone():
                    # update
                    cursor.execute(
                        "UPDATE courses_coursemasterdisplay SET screen_order=%s, rating=%s WHERE course_master_id=%s",
                        [order, rating, course_id]
                    )
                else:
                    # insert
                    cursor.execute(
                        "INSERT INTO courses_coursemasterdisplay (course_master_id, screen_order, rating) VALUES (%s, %s, %s)",
                        [course_id, order, rating]
                    )

        return JsonResponse({"status": "success", "msg": "Done"})

    except Exception as e:
        return JsonResponse({"status": "failed", "msg": str(e)}, status=500)


@csrf_exempt
def registration_user_msg(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Print to your console for testing
            print("Webhook Received:", data)
            
            # TODO: Add your logic here (e.g., saving to database)
            
            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'invalid json'}, status=400)
            
    return JsonResponse({'status': 'method not allowed'}, status=405)