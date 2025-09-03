import razorpay
from courses.models import CoursePurchased, Course, VideoFiles, UserWatch, CourseMaster, MonthMoney, FileType
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
import hashlib
from homepage.models import Lookup, CouponCode
import os
import qrcode
from django.urls import reverse

from demo.models import UploadDemo

from demo.models import AddUserDemoCode, MainUserDemo

from demo.models import BulkCode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from common_function.send_message import send_sms
from django.http import HttpResponse
from accounts.models import UserProfile
import json, base64, hashlib
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def calculate_future_date(month):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=30 * month)  # Assuming a month has 30 days for simplicity
    return future_date


def homepage(request, id=0):
    user_id = request.session.get('user_id')
    if id != 0:
        course_master1 = Course.objects.filter(course_master_id=id)
        course_master2 = ''
        course_master3 = ''
        course_master4 = ''
        course_master5 = ''
    else:
        course_master1 = CourseMaster.objects.filter(ScreenColumn__screen_column=1).order_by('-id')
        course_master2 = CourseMaster.objects.filter(ScreenColumn__screen_column=2).order_by('-id')
        course_master3 = CourseMaster.objects.filter(ScreenColumn__screen_column=3).order_by('-id')
        course_master4 = CourseMaster.objects.filter(ScreenColumn__screen_column=4).order_by('-id')
        course_master5 = CourseMaster.objects.filter(ScreenColumn__screen_column=5).order_by('-id')

    demo_file_path = ''
    demo_file = UploadDemo.objects.filter().order_by('-id')
    if demo_file:
        demo_file_path = demo_file[0].file.url

    bulk_code = BulkCode.objects.filter(Q()).order_by('id')
    if bulk_code:
        bulk_code = bulk_code[0].code

    context = {
        'id': id,
        'course_master1': course_master1,
        'course_master2': course_master2,
        'course_master3': course_master3,
        'course_master4': course_master4,
        'course_master5': course_master5,
        'demo_file': demo_file_path,
        'bulk_code': bulk_code,
        'user_id': user_id,
    }
    return render(request, 'index.html', context)


def send_order_confirmation_email(order):
    try:
        subject = 'Order Confirmation'
        try:
            to_email = order[0].user.email
        except:
            to_email = order[0].user.username + '@yopmail.com'
        from_email = 'mrctherapy2023@gmail.com'

        # Render the email template
        email_content = render_to_string('order_confirmation_email.html', {
            'customer_name': order[0].user.first_name,
            'order_items': order[0].course.name,
            'mrp_price': order[0].price,
            'discount': order[0].discount,
            'total_amount': order[0].totalprice,
            'razorpay_payment_id': order[0].razorpay_payment_id,
            'razorpay_order_id': order[0].razorpay_order_id,
        })

        # Create and send email
        email = EmailMessage(subject, email_content, from_email, [to_email])
        email.content_subtype = 'html'  # Set email content type to HTML
        email.send()
    except:
        pass


@login_required(login_url='/accounts/login/')
def my_courses(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        is_admin = User.objects.filter(id=user_id, username='admin')
        if is_admin:
            query = Q()
        else:
            query = Q(user_id=user_id) & Q(payment_status='success') | Q(user_id=user_id) & Q(payment_status='renew')
            course_purchased = CoursePurchased.objects.filter(query).values_list('course', flat=True)
            query = Q(id__in=course_purchased)
        my_pur_cours = Course.objects.filter(query)
        context = {'my_course': my_pur_cours}
        return render(request, 'my_course.html', context)
    else:
        return redirect('/accounts/login/')


def watch_video(request, pre_next='', type='', course_id=0, file_id=0):
    now_date = datetime.now()
    now_date = now_date.strftime("%Y-%m-%d")

    user_id = request.session.get('user_id')
    type = type
    course_id = course_id
    file_type = ''
    try:
        thumb = Lookup.objects.get(code='common thumb')
    except:
        thumb = ''

    if user_id is not None:
        is_admin = User.objects.filter(id=user_id, username='admin')
        if is_admin:
            if type == 'professional':
                video_files = VideoFiles.objects.filter(course_id=course_id)
                context = {'type': type,
                           'data': video_files,
                           'thumb': thumb,
                           }
                return render(request, 'course-details.html', context)

            elif type == 'regular':
                video_files = VideoFiles.objects.filter(course_id=course_id)
                context = {'type': type,
                           'data': video_files,
                           'thumb': thumb,
                           }
                return render(request, 'regular.html', context)

            else:
                watch_video_ids = UserWatch.objects.filter(user_id=user_id, status='complete',
                                                           course_id=course_id).values_list('videofile', flat=True)
                if watch_video_ids:
                    if file_id != 0:
                        if pre_next == 'pre':
                            video_path = VideoFiles.objects.filter(course_id=course_id, id__lt=file_id)[0]
                            if video_path:
                                file_id = video_path.id
                                file_type = video_path.file_type.file_type
                        else:
                            if pre_next == 'next':
                                video_path = VideoFiles.objects.filter(course_id=course_id, id__gt=file_id)[0]
                                if video_path:
                                    file_id = video_path.id
                                    file_type = video_path.file_type.file_type
                    else:
                        try:
                            video_path = VideoFiles.objects.filter(course_id=course_id).exclude(id__in=watch_video_ids)[
                                0]
                            file_id = video_path.id
                            file_type = video_path.file_type.file_type
                        except:
                            file_id = 0
                            video_path = ''
                else:
                    try:
                        video_path = VideoFiles.objects.filter(course_id=course_id)[0]
                        file_id = video_path.id
                        file_type = video_path.file_type.file_type
                    except:
                        file_id = 0
                        video_path = ''
                context = {
                    'pre_next': pre_next,
                    'data': video_path,
                    'file_type': file_type,
                    'course_id': course_id,
                    'file_id': file_id
                }
                return render(request, 'common.html', context)
        else:
            is_exipre = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
            if is_exipre:
                mail_delivered = is_exipre[0].mail_delivered
                if mail_delivered == False:
                    send_order_confirmation_email(is_exipre)
                    CoursePurchased.objects.filter(user_id=user_id, course_id=course_id).update(mail_delivered=True)
                expire_date = is_exipre[0].end_date.strftime("%Y-%m-%d")
                if now_date > expire_date:
                    status = 'renew'
                    CoursePurchased.objects.filter(user_id=user_id, course_id=course_id).update(payment_status=status)
                    return redirect(f'/buy_course_detail/{course_id}/{status}/')

                payment_status = is_exipre[0].payment_status
                if payment_status == 'renew':
                    status = 'renew'
                    return redirect(f'/buy_course_detail/{course_id}/{status}/')

                if now_date < expire_date and payment_status == 'success':
                    if type == 'professional':
                        video_files = VideoFiles.objects.filter(course_id=course_id)
                        context = {'type': type,
                                   'data': video_files,
                                   'thumb': thumb,
                                   }
                        return render(request, 'course-details.html', context)

                    elif type == 'regular':
                        video_files = VideoFiles.objects.filter(course_id=course_id)
                        context = {'type': type,
                                   'data': video_files,
                                   'thumb': thumb,
                                   }
                        return render(request, 'regular.html', context)

                    else:
                        watch_video_ids = UserWatch.objects.filter(user_id=user_id, status='complete',
                                                                   course_id=course_id).values_list('videofile',
                                                                                                    flat=True)
                        if watch_video_ids:
                            if file_id != 0:
                                if pre_next == 'pre':
                                    video_path = VideoFiles.objects.filter(course_id=course_id, id__lt=file_id)[0]
                                    if video_path:
                                        file_id = video_path.id
                                        file_type = video_path.file_type.file_type
                                else:
                                    if pre_next == 'next':
                                        video_path = VideoFiles.objects.filter(course_id=course_id, id__gt=file_id)[0]
                                        if video_path:
                                            file_id = video_path.id
                                            file_type = video_path.file_type.file_type
                            else:
                                try:
                                    video_path = \
                                        VideoFiles.objects.filter(course_id=course_id).exclude(id__in=watch_video_ids)[
                                            0]
                                    file_id = video_path.id
                                    file_type = video_path.file_type.file_type
                                except:
                                    file_id = 0
                                    video_path = ''
                        else:
                            try:
                                video_path = VideoFiles.objects.filter(course_id=course_id)[0]
                                file_id = video_path.id
                                file_type = video_path.file_type.file_type
                            except:
                                file_id = 0
                                video_path = ''
                        context = {
                            'pre_next': pre_next,
                            'data': video_path,
                            'file_type': file_type,
                            'course_id': course_id,
                            'file_id': file_id
                        }
                        return render(request, 'common.html', context)
    else:
        redirect('/accounts/login/')


def count_video(request, id):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        if user_id is not None:
            count = int(form.get('count', None))
            video_id = id
            watch_obj = ''
            status = ''
            msg = ''
            try:
                video_obj = VideoFiles.objects.get(id=video_id)
                course = Course.objects.get(name__iexact=video_obj.course)
                course_id = course.id
                already_watch = UserWatch.objects.filter(user_id=user_id, course_id=course_id, videofile_id=video_id)
                if already_watch:
                    for already_watch in already_watch:
                        pre_count = already_watch.whatch_count
                        already_watch.whatch_count = count + pre_count
                        already_watch.status = 'complete'
                        already_watch.save()
                        status = 1
                else:
                    watch_obj = UserWatch.objects.create(user_id=user_id, course_id=course_id, videofile_id=video_id,
                                                         whatch_count=count, status='incomplete', )
                    if watch_obj:
                        msg = 'user watched video successfully'
                        status = 1
            except Exception as e:
                print(e, '=====================error in count_video function')
                msg = 'user not watched video successfully'

            json_data = {'msg': msg, 'status': status}
            return JsonResponse(json_data)
        return redirect('/accounts/login/')


def round_view(request, video_id):
    form = request.GET
    user_id = request.session.get('user_id')
    count = int(form.get('count', None))

    video_obj = VideoFiles.objects.get(id=video_id)
    course = Course.objects.get(name__iexact=video_obj.course)
    course_id = course.id

    status = ''
    msg = ''
    user_watch_video = ''

    try:
        user_watch_video = UserWatch.objects.get(user_id=user_id, videofile_id=video_id)
    except Exception as e:
        print(e, '=================e=================')

    if user_watch_video:
        whatch_count = user_watch_video.whatch_count
        round_view = video_obj.round_view
        if round_view > whatch_count:
            user_watch_video.whatch_count = int(whatch_count) + count
            user_watch_video.save()
            status = 1
            msg = 'Updated user_watched entry'

    else:
        watch_obj = UserWatch.objects.create(user_id=user_id, course_id=course_id, videofile_id=video_id,
                                             whatch_count=count, status='incomplete', )
        if watch_obj:
            status = 0
            msg = 'Created user_watched entry'

    context = {
        'status': status,
        'msg': msg,
    }
    return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def add_course(request):
    file_type = FileType.objects.all()
    course = Course.objects.all()

    context = {
        'file_type': file_type,
        'course': course,
    }
    return render(request, 'add_course.html', context)


@login_required(login_url='/accounts/login/')
def upload_video(request):
    if request.method == 'POST':
        form = request.POST
        form1 = request.FILES
        file_type = form.get('file_type')
        course = form.get('courseName')
        video = form1.getlist('videoFile')
        pro_count = 0
        try:
            for i in range(len(video)):
                # pro_count = VideoFiles.objects.filter(course_id=4).count()
                pro_count += 1
                new_product = VideoFiles.objects.create(file_type_id=file_type,
                                                        course_id=course,
                                                        day=pro_count,
                                                        title=video[i],
                                                        file=video[i],
                                                        # code_no=pro_count,
                                                        )
                # if new_product:
                # video_detail_url = request.build_absolute_uri(reverse('video_detail', args=[pro_count]))
                #
                # qr = qrcode.QRCode(version=1,
                #                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                #                    box_size=10,
                #                    border=4,
                #                    )
                # qr.add_data(video_detail_url)
                # qr.make(fit=True)
                #
                # img = qr.make_image(fill_color="black", back_color="white")
                #
                # qr_codes_dir = os.path.join(BASE_DIR, 'media', 'qr_codes')
                # os.makedirs(qr_codes_dir, exist_ok=True)
                #
                # qr_code_path = f"qr_codes/video_{pro_count}.png"
                # img.save(os.path.join(BASE_DIR, 'media', qr_code_path))
                #
                # new_product.qr_code = qr_code_path
                # new_product.save()
            status = 'success'
            msg = 'video files uploaded.'
        except Exception as e:
            msg = str(e)
            status = 'error'

    context = {
        'status': status,
        'msg': msg,
    }
    return JsonResponse(context)


def video_detail(request, id):
    video = VideoFiles.objects.get(code_no=id)
    context = {
        'video': video,
    }
    return render(request, 'video_detail.html', context)


@login_required(login_url='/accounts/login/')
def view_list(request, course_id):
    context = {
        'course_id': course_id,
    }
    return render(request, 'view_list_kshar_sutra.html', context)


@login_required(login_url='/accounts/login/')
def get_kshar_sutra_videos(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        video_list = []
        videos = VideoFiles.objects.filter(course_id=course_id)
        for i in videos:
            video_dict = {}
            video_dict['id'] = i.id
            video_dict['file_type'] = i.file_type.file_type
            video_dict['course'] = i.course.name
            video_dict['day'] = i.day if i.day else ''
            video_dict['title'] = i.title if i.title else ''
            video_dict['code_no'] = i.code_no if i.code_no else ''
            video_list.append(video_dict)
        context = {
            'video_list': video_list
        }
        return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def delete_files(request):
    video_id = request.GET.get('video_id')
    try:
        video = VideoFiles.objects.get(id=video_id)

        try:
            video_file_path = video.file.url
            video_file_path = os.path.join(BASE_DIR + video_file_path)
            if os.path.exists(video_file_path):
                os.remove(video_file_path)
        except Exception as e:
            print(e)

        try:
            qr_code_file_path = video.qr_code.url
            qr_code_file_path = os.path.join(BASE_DIR + qr_code_file_path)
            if os.path.exists(qr_code_file_path):
                os.remove(qr_code_file_path)
        except Exception as e:
            print(e)

        video.delete()

        status = 'success'
        msg = 'Deleted file.'
    except Exception as e:
        print(e)
        status = 'error'
        msg = 'No file deleted!'
    context = {
        'status': status,
        'msg': msg,
    }
    return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def payment_success(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        form = request.GET
        razorpay_order_id = form.get('razorpay_order_id', None)
        razorpay_payment_id = form.get('razorpay_payment_id', None)
        razorpay_signature = form.get('razorpay_signature', None)
        course_id = form.get('course_id', None)
        totalprice = int(float(form.get('totalprice', None)))
        payment_status = form.get('payment_status', None)
        status = 0

        try:
            query = Q(user_id=user_id, course_id=course_id, razorpay_order_id=razorpay_order_id)
            course_obj = CoursePurchased.objects.filter(query).update(totalprice=totalprice,
                                                                      razorpay_payment_id=razorpay_payment_id,
                                                                      razorpay_signature=razorpay_signature,
                                                                      payment_status=payment_status,
                                                                      start_date=datetime.now()
                                                                      )
            if course_obj:
                order = CoursePurchased.objects.filter(query)
                mobile = order[0].user.mobile
                send_order_confirmation_email(order)
                CoursePurchased.objects.filter(query).update(mail_delivered=True)
                status = 1
                message = f'Thank you for choosing {status} MRC therapy (Inventor Dr. Abhishek Sharma) MRC AYURVEDA & RESEARCH CENTER'
                send_sms(mobile, message)
        except Exception as e:
            print(e, '=====error in payment success function')
            status = 0
        json_data = {'status': status}

        return JsonResponse(json_data)


@login_required(login_url='/accounts/login/')
def get_service_month(request):
    if request.method == 'GET':
        form = request.GET
        course_id = form.get('course_id')
        price_data = MonthMoney.objects.filter(course_id=course_id).order_by('month')
        data_list = []
        if price_data:
            for i in price_data:
                data_dict = {}
                data_dict['id'] = i.id
                data_dict['month'] = i.month
                data_dict['price'] = i.money
                data_list.append(data_dict)

        context = {
            'data': data_list
        }
        return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def get_service_price(request):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        course_id = form.get('course_id')
        month_id = form.get('month_id')
        data_dict = {}
        price_data = MonthMoney.objects.get(id=month_id)

        data_dict['month'] = price_data.month
        data_dict['price'] = price_data.money

        future_date = calculate_future_date(data_dict['month'])
        same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
        if same_user:
            CoursePurchased.objects.filter(user_id=user_id, course_id=course_id, ).update(price=data_dict['price'],
                                                                                          totalprice=data_dict['price'],
                                                                                          month=data_dict['month'],
                                                                                          start_date=datetime.now(),
                                                                                          end_date=future_date)
        else:
            CoursePurchased.objects.create(user_id=user_id,
                                           course_id=course_id,
                                           price=data_dict['price'],
                                           totalprice=data_dict['price'],
                                           month=data_dict['month'],
                                           end_date=future_date
                                           )

        context = {
            'data': data_dict,
            'course_id': course_id
        }
        return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def apply_coupon_code(request):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        course_id = form.get('course_id')
        coupon_code = form.get('coupon_code')
        coupon_data = CouponCode.objects.filter(coupon_code__exact=coupon_code)
        coupon_dict = {}
        if coupon_data:
            coupon_dict['percent'] = coupon_data[0].percent
            coupon_dict['coupon_code'] = coupon_data[0].coupon_code

        same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
        if same_user:
            try:
                CoursePurchased.objects.filter(user_id=user_id, course_id=course_id).update(
                    discount=coupon_dict['percent'],
                    coupon_code=coupon_dict['coupon_code'],
                    start_date=datetime.now(),
                )
            except Exception as e:
                print(e, '===========e===============')
                CoursePurchased.objects.filter(user_id=user_id, course_id=course_id).update(discount=0,
                                                                                            coupon_code='',
                                                                                            start_date=datetime.now(),
                                                                                            )
        context = {
            'coupon_data': coupon_dict
        }
        return JsonResponse(context)


def gargi(request):
    page_reload = Lookup.objects.filter(code='page_reload')
    if page_reload:
        page_reload = page_reload[0].desc
    else:
        page_reload = 20
    course_query = CoursePurchased.objects.filter().exclude(payment_status='success').order_by('-start_date')[:100]
    context = {
        'course_query': course_query,
        'page_reload': page_reload,
    }
    return render(request, 'customer/customer_course_purchased.html', context)


def search_therapy(request):
    q = request.GET.get('q', '')
    results = []

    if q:
        therapies = Course.objects.filter(name__icontains=q)[:10]  # Limit for performance
        results = [{'id': t.id, 'name': t.name} for t in therapies]
    return JsonResponse({'results': results})


@csrf_exempt  # If you're not passing CSRF token, else remove this
def final_pay(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        course_id = request.POST.get('course_id')
        data = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
        if data:
            try:
                user = UserProfile.objects.filter(user_id=user_id)
                mobile = user[0].mobile
                course = data[0].course.name
                message = f'Congratulations you have enrolled {course} MRC therapy (Inventor Dr. Abhishek Sharma) MRC AYURVEDA & RESEARCH CENTER'
                send_sms(mobile, message)
                status = 'success'
                send_sms('9267678888', message)
            except:
                message = f'Hope you are enjoy MRC therapy if any problem please contact {9267678888} this number (Inventor Dr. Abhishek Sharma) MRC AYURVEDA & RESEARCH CENTER'
                user = UserProfile.objects.filter(user_id=user_id)
                mobile = user[0].mobile
                send_sms(mobile, message)
                status = 'failed!'
            context = {
                'status': status,
            }
            return JsonResponse(context)


# -----------------------------------------
@login_required(login_url='/accounts/login/')
def buy_course_detail(request, course_id, status=None):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        form = request.POST
        apply_coupon = form.get('apply_coupon')
        month = form.get('month')
        course_id = course_id
        discount = 0
        course_price = MonthMoney.objects.filter(course_id=course_id, month=month)
        if course_price:
            base_price = course_price[0].money
        else:
            course_price = MonthMoney.objects.filter(course_id=course_id)[0]
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
        # context = {
        #     'course_price': base_price,
        #     'totalprice': course_price,
        #     'discount': discount,
        #     'month': month,
        #     'course_id': course_id,
        #     'user_id': user_id,
        # }

        url = "https://api.phonepe.com/apis/identity-manager/v1/oauth/token"

        payload = {
            "client_version": 1,
            "grant_type": "client_credentials",
            "client_id": "SU2508121540161685954553",
            "client_secret": "ffb3222b-725d-4fdb-9261-98b32bf0b5c7",
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=payload, headers=headers)
        data = response.json()
        access_token = data.get("access_token")
        try:
            final_payload = {
                "merchantOrderId": generate_tran_id(),
                "amount": course_price * 100,
                "expireAfter": 1200,
                "metaInfo": {
                    "udf1": "test1",
                    "udf2": "new param2",
                    "udf3": "test3",
                    "udf4": "dummy value 4",
                    "udf5": "addition infor ref1"
                },
                "paymentFlow": {
                    "type": "PG_CHECKOUT",
                    "message": "Payment message used for collect requests",
                    "merchantUrls": {
                        "redirectUrl": "https://mrctherapy.com/my-courses/"
                    }

                }
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"O-Bearer {access_token}"
            }

            url = 'https://api.phonepe.com/apis/pg/checkout/v2/pay'
            response = requests.post(url, headers=headers, json=final_payload)

            response = response.json()
            orderId = response.get("orderId")
            same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)

            try:
                if same_user:
                    CoursePurchased.objects.filter(user_id=user_id, course_id=course_id).update(
                        razorpay_order_id=orderId,
                        access_token=access_token,
                        totalprice=course_price,
                        discount=discount,
                        start_date=datetime.now()
                        )
                else:
                    CoursePurchased.objects.create(user_id=user_id, razorpay_order_id=orderId,access_token=access_token, course_id=course_id,
                                                   totalprice=course_price, discount=discount)
            except:
                pass

            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    else:
        course_data = Course.objects.get(id=course_id)

        already_purchased = CoursePurchased.objects.filter(course_id=course_id, user_id=user_id,
                                                           payment_status='success')
        if already_purchased:
            return redirect('/')

        context = {
            'status': status,
            'course_data': course_data,
            'course_id': course_id,
        }
        return render(request, 'new_cart_page.html', context)


def generate_tran_id():
    """Generate unique merchantTransactionId (you can replace this logic)."""
    import uuid
    return "TID" + str(uuid.uuid4().hex[:12])


@csrf_exempt
def initiate_payment(request):
    amount = int(request.GET.get('totalprice'))
    url = "https://api.phonepe.com/apis/identity-manager/v1/oauth/token"

    payload = {
        "client_version": 1,
        "grant_type": "client_credentials",
        "client_id": "SU2508121540161685954553",
        "client_secret": "ffb3222b-725d-4fdb-9261-98b32bf0b5c7",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    data = response.json()
    access_token = data.get("access_token")
    try:
        final_payload = {
            "merchantOrderId": generate_tran_id(),
            "amount": amount * 100,
            "expireAfter": 1200,
            "metaInfo": {
                "udf1": "test1",
                "udf2": "new param2",
                "udf3": "test3",
                "udf4": "dummy value 4",
                "udf5": "addition infor ref1"
            },
            "paymentFlow": {
                "type": "PG_CHECKOUT",
                "message": "Payment message used for collect requests",
                "merchantUrls": {
                    "redirectUrl": "https://mrctherapy.com/my-courses/"
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"O-Bearer {access_token}"
        }

        url = 'https://api.phonepe.com/apis/pg/checkout/v2/pay'
        response = requests.post(url, headers=headers, json=final_payload)

        response = response.json()
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"error": str(e)})


@csrf_exempt
def payment_callback(request):
    data = request.POST or request.body
    print("CALLBACK DATA:", data)
    # Verify checksum if needed
    return JsonResponse({"status": "ok"})
