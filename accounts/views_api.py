from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
import random
import requests
from .models import UserProfile, OtpVerify
from .whatsapp import send_whatsapp_registration_msg




# whatsappp registration me


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('username')
        username = username.strip()
        password = form.get('password')
        password = password.strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            user_id = user.id
            msg = 'User logged in successfully'
            status = 'success'
        else:
            user_id = 0
            msg = 'User name or password is not correct!'
            status = 'failed'

        json_data = {
            'user_id': user_id,
            'msg': msg,
            'status': status
        }

        return JsonResponse(json_data)


@csrf_exempt
def user_logout(request):
    logout(request)
    msg = 'User logged out successfully'
    status = 'success'

    json_data = {
        'msg': msg,
        'status': status
    }
    return JsonResponse(json_data)


@csrf_exempt
def app_register(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'failed',
            'msg': 'Method not allowed'
        }, status=405)

    full_name = (request.POST.get('full_name') or request.POST.get('fullname') or '').strip()
    phone = (request.POST.get('phone') or request.POST.get('contact_number') or '').strip()
    email = (request.POST.get('email') or '').strip().lower()
    password = (request.POST.get('password') or '').strip()
    address = (request.POST.get('address') or '').strip()

    if not full_name or not phone or not email or not password:
        return JsonResponse({
            'status': 'failed',
            'msg': 'full_name, phone, email and password are required'
        }, status=400)

    username = phone[-10:]

    query = Q(username=username) | Q(email=email)
    existing_user = User.objects.filter(query).exists()

    if existing_user:
        return JsonResponse({
            'status': 'failed',
            'msg': 'This User Already Exists.'
        }, status=409)

    try:
        user = User.objects.create_user(username)
        user.set_password(password)
        user.first_name = full_name
        user.email = email
        user.save()

        UserProfile.objects.create(
            user_id=user.id,
            mobile=phone,
            address=address,
        )
        try: 
            send_whatsapp_registration_msg(phone, full_name)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {str(e)}") 

        return JsonResponse({
            'status': 'success',
            'msg': 'User registration successfully.',
            'user': {
                'user_id': user.id,
                'username': user.username or '',
                'email': user.email or '',
                'full_name': user.first_name or '',
                'phone': phone,
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'failed',
            'msg': str(e)
        }, status=500)


@csrf_exempt
def app_login(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'failed',
            'msg': 'Method not allowed'
        }, status=405)

    identifier = (request.POST.get('identifier') or request.POST.get('email') or '').strip()
    password = (request.POST.get('password') or '').strip()

    if not identifier or not password:
        return JsonResponse({
            'status': 'failed',
            'msg': 'identifier and password are required'
        }, status=400)

    query = Q(username=identifier[-10:]) | Q(email=identifier)
    users = User.objects.filter(query)

    if not users:
        return JsonResponse({
            'status': 'failed',
            'msg': 'User not found'
        }, status=404)

    user = authenticate(request, username=users[0].username, password=password)

    if user is None:
        return JsonResponse({
            'status': 'failed',
            'msg': 'User name or password is not correct!'
        }, status=401)

    login(request, user)
    request.session['user_id'] = user.id

    profile = UserProfile.objects.filter(user_id=user.id).first()

    return JsonResponse({
        'status': 'success',
        'msg': 'User logged in successfully',
        'user': {
            'user_id': user.id,
            'username': user.username or '',
            'email': user.email or '',
            'full_name': user.first_name or '',
            'phone': profile.mobile if profile and profile.mobile else '',
	    'is_staff': user.is_staff,
        }
    })


@csrf_exempt
def app_me(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return JsonResponse({
            'status': 'failed',
            'msg': 'Not authenticated'
        }, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'failed',
            'msg': 'User not found'
        }, status=404)

    profile = UserProfile.objects.filter(user_id=user.id).first()

    return JsonResponse({
        'status': 'success',
        'user': {
            'user_id': user.id,
            'username': user.username or '',
            'email': user.email or '',
            'full_name': user.first_name or '',
            'phone': profile.mobile if profile and profile.mobile else '',
            'is_staff': user.is_staff,
        }
    })


@csrf_exempt
def app_logout(request):
    logout(request)
    request.session.flush()

    return JsonResponse({
        'status': 'success',
        'msg': 'User logged out successfully'
    })

@csrf_exempt
def app_change_password(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'failed',
            'msg': 'Method not allowed'
        }, status=405)

    session_user_id = request.session.get('user_id')
    user_id = session_user_id or request.POST.get('user_id')

    if not user_id:
        return JsonResponse({
            'status': 'failed',
            'msg': 'Not authenticated'
        }, status=401)

    current_password = (request.POST.get('current_password') or '').strip()
    new_password = (request.POST.get('new_password') or '').strip()

    if not current_password or not new_password:
        return JsonResponse({
            'status': 'failed',
            'msg': 'current_password and new_password are required'
        }, status=400)

    if len(new_password) < 6:
        return JsonResponse({
            'status': 'failed',
            'msg': 'New password must be at least 6 characters'
        }, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'failed',
            'msg': 'User not found'
        }, status=404)

    auth_user = authenticate(request, username=user.username, password=current_password)

    if auth_user is None:
        return JsonResponse({
            'status': 'failed',
            'msg': 'Current password is incorrect'
        }, status=401)

    user.set_password(new_password)
    user.save()

    if session_user_id:
        try:
            update_session_auth_hash(request, user)
        except Exception:
            pass

    return JsonResponse({
        'status': 'success',
        'msg': 'Password changed successfully'
    }, status=200)


# otp foreget password
def generate_otp():
    return f"{random.randint(0, 999999):06d}"


def send_sms_otp(phone, otp):
    url = "http://msg.icloudsms.com/rest/services/sendSMS/sendGroupSms"

    querystring = {
        "AUTH_KEY": "3380567192fd2e6d18f63985aace",
        "message": (
            "Namaste!!\n"
            "Welcome to MRC Ayurveda, Access your more Details \n"
            "www.MrcAyurveda.com\n"
            f"Using User ID {phone}\n"
            f"Password {otp}"
        ),
        "senderId": "MRCARC",
        "routeId": "1",
        "mobileNos": phone,
        "smsContentType": "english",
    }

    headers = {
        "Cache-Control": "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring, timeout=15)
    print("SMS status code:", response.status_code)
    print("SMS raw response:", response.text)
    return response.text

@csrf_exempt
def app_forgot_password_send_otp(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    phone = (request.POST.get("phone") or "").strip()
    phone = phone[-10:]

    if len(phone) != 10 or not phone.isdigit():
        return JsonResponse({"status": "failed", "msg": "Enter a valid 10-digit phone number"}, status=400)

    profile = UserProfile.objects.filter(mobile__endswith=phone).select_related("user").first()
    if not profile or not profile.user_id:
        return JsonResponse({"status": "failed", "msg": "No account found for this phone number"}, status=404)

    otp = generate_otp()

    OtpVerify.objects.update_or_create(
        email=profile.user.email,
        defaults={
            "mobile": phone,
            "otp": otp,
            "updated_at": timezone.now().date(),
        },
    )

    try:
        send_sms_otp(phone, otp)
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": f"Unable to send OTP: {str(e)}"}, status=500)

    return JsonResponse({"status": "success", "msg": "OTP sent successfully"})


@csrf_exempt
def app_forgot_password_reset(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed", "msg": "Method not allowed"}, status=405)

    phone = (request.POST.get("phone") or "").strip()
    otp = (request.POST.get("otp") or "").strip()
    new_password = (request.POST.get("new_password") or "").strip()

    phone = phone[-10:]

    if len(phone) != 10 or not phone.isdigit():
        return JsonResponse({"status": "failed", "msg": "Enter a valid 10-digit phone number"}, status=400)

    if len(otp) != 6 or not otp.isdigit():
        return JsonResponse({"status": "failed", "msg": "Enter valid 6-digit OTP"}, status=400)

    if len(new_password) < 6:
        return JsonResponse({"status": "failed", "msg": "Password must be at least 6 characters"}, status=400)

    profile = UserProfile.objects.filter(mobile__endswith=phone).select_related("user").first()
    if not profile or not profile.user_id:
        return JsonResponse({"status": "failed", "msg": "No account found for this phone number"}, status=404)

    otp_row = OtpVerify.objects.filter(
        email__iexact=profile.user.email,
        mobile=phone,
        otp=otp,
    ).first()

    if not otp_row:
        return JsonResponse({"status": "failed", "msg": "Invalid OTP"}, status=400)

    user = profile.user
    user.set_password(new_password)
    user.save()

    OtpVerify.objects.filter(email__iexact=profile.user.email).delete()

    return JsonResponse({"status": "success", "msg": "Password reset successfully"})
