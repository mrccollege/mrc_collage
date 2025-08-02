import time
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from homepage.models import Lookup
from django.core.mail import send_mail
# Create your views here.
from .models import UserQuery, OtpVerify, UserProfile
from twilio.rest import Client
from django.db.models import Q

# from common_function.send_message import send_sms

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_sms(mobile, message):
    url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
    print(mobile, '===============####################')
    print(message, '===============####################')
    params = {
        'AUTH_KEY': '3380567192fd2e6d18f63985aace',
        'message': message,
        'senderId': 'MRCARC',
        'routeId': 1,
        'mobileNos': mobile,
        'smsContentType': 'english'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response to a Python dict
        response_code = data.get('responseCode')
        response_value = data.get('response')

        # Now you can use the values
        print("Response Code:", response_code)
        print("Response:", response_value)
    else:
        print("Failed to send SMS", response.text)


def register_account(request):
    if request.method == 'POST':
        form = request.POST
        first_name = form.get('fullname')
        first_name.strip()

        username = form.get('contact_number')
        username.strip()
        username = username[-10:]

        email = form.get('email')
        email.strip()

        password = form.get('password')
        password = password.strip()

        address = form.get('address')
        contact_number = form.get('contact_number')
        query = Q(username=username) | Q(email=email)
        try:
            user = User.objects.filter(query).exists()
            if user:
                msg = 'This User Already Exists.'
                id = 0

                data_json = {
                    'id': id,
                    'msg': msg,
                }

                return JsonResponse(data_json)
            user = User.objects.create_user(username)
            if user is not None:
                user.set_password(password)
                user.first_name = first_name
                user.email = email
                user.save()
                id = user.id
                UserProfile.objects.create(user_id=id,
                                           mobile=contact_number,
                                           address=address,
                                           )
                msg = 'User registration successfully.'
        except Exception as e:
            msg = str(e)
            id = 0

        data_json = {
            'id': id,
            'msg': msg,
        }

        return JsonResponse(data_json)

    else:
        try:
            home_banner = Lookup.objects.get(code='home_banner')
        except:
            home_banner = ''
        context = {'home_banner': home_banner}
        return render(request, 'user_register.html', context)


def login_account(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('email')
        username = username.strip()
        password = form.get('password')
        password = password.strip()

        query = Q(username=username[-10:]) | Q(email=username)
        user = User.objects.filter(query)
        if user:
            user = authenticate(request, username=user[0].username, password=password)

            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                msg = 'User logged in successfully'
                status = 'success'
            else:
                msg = 'User name or password is not correct!'
                status = 'failed'

            json_data = {
                'msg': msg,
                'status': status
            }

            return JsonResponse(json_data)
        else:
            try:
                home_banner = Lookup.objects.get(code='home_banner')
            except:
                home_banner = ''

            context = {'home_banner': home_banner}
            return render(request, 'login_page.html', context)
    else:
        try:
            home_banner = Lookup.objects.get(code='home_banner')
        except:
            home_banner = ''

        context = {'home_banner': home_banner}
        return render(request, 'login_page.html', context)


def logout_account(request):
    logout(request)
    return redirect('/accounts/login/')


def generate_time_based_otp():
    # Get the current time in seconds
    current_time = int(time.time())
    # Convert the current time to a string and use a portion of it as the OTP
    otp = str(current_time)[-6:]

    return otp


def send_otp_email(email, otp):
    subject = 'Your OTP for Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'sanjay.singh@crebritech.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def forget_password(request):
    if request.method == 'POST':
        form = request.POST
        email = form.get('email')
        is_user = User.objects.filter(email__exact=email)
        if is_user:
            otp = generate_time_based_otp()
            otp_obj = OtpVerify.objects.filter(email__exact=email)
            if otp_obj:
                OtpVerify.objects.filter(email__exact=email).update(otp=otp)
                send_otp_email(email, otp)
                status = 1
                msg = f'OTP Send successfully on {email}'
            else:
                try:
                    OtpVerify.objects.create(email=email, otp=otp)
                    send_otp_email(email, otp)
                    status = 1
                    msg = f'OTP Send successfully on {email}'
                except Exception as e:
                    status = 0
                    msg = str(e)
        else:
            status = 0
            msg = 'Email is not registered'

        context = {
            'status': status,
            'msg': msg,
            'email': email,
        }
        return JsonResponse(context)
    return render(request, 'forget_password.html')


def verity_otp(request, email=None):
    if request.method == 'POST':
        form = request.POST
        email = form.get('email')
        otp = form.get('otp')
        new_password = form.get('new_password')
        status = 0
        msg = 'Password not reset'
        is_user = User.objects.filter(email__iexact=email)
        if is_user:
            otp_obj = OtpVerify.objects.filter(email__iexact=email, otp__iexact=otp)
            if otp_obj:
                users = User.objects.filter(email__iexact=email)
                user = users[0]
                user.set_password(new_password)
                user.save()
                status = 1
                msg = 'Password successfully reset'
                OtpVerify.objects.filter(email__iexact=email).delete()
            else:
                status = 0
                msg = msg

        context = {
            'status': status,
            'msg': msg,
            'email': email,
        }
        return JsonResponse(context)

    context = {
        'email': email
    }
    return render(request, 'verity_otp.html', context)


def term_condition(request):
    logout(request)
    return render(request, 'term_condition.html')


def cancel_refund(request):
    logout(request)
    return render(request, 'cancel_refund.html')


def shiping(request):
    logout(request)
    return render(request, 'shiping.html')


def privacy_policy(request):
    logout(request)
    return render(request, 'privacy_policy.html')


def contact_us(request):
    if request.method == 'POST':
        form = request.POST
        name = form.get('name')
        whatsapp = form.get('whatsapp')
        email = form.get('email')
        message = form.get('message')
        status = 0
        try:
            q_obj = UserQuery.objects.create(name=name,
                                             whatsapp=whatsapp,
                                             email=email,
                                             message=message,
                                             )

            try:
                recipient_numbers = ['whatsapp:+917351154123', 'whatsapp:+918279408396', 'whatsapp:+919267678888']
                message = client.messages.create(
                    body=f'Name: {name}, '
                         f'whatsapp: {whatsapp}, '
                         f'email: {email}, '
                         f'message: {message} ',
                    from_='whatsapp:' + settings.TWILIO_PHONE_NUMBER,
                    to=recipient_numbers
                )
            except Exception as e:
                print(e)

            if q_obj:
                status = 1
        except:
            pass

        context = {
            'status': status
        }
        return JsonResponse(context)

    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''

    context = {
        'home_banner': home_banner,
    }
    return render(request, 'contact_us.html', context)
