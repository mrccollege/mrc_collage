from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from homepage.models import Lookup

# Create your views here.
from .models import UserQuery


def register_account(request):
    if request.method == 'POST':
        form = request.POST
        first_name = form.get('fullname')
        first_name.strip()

        usename = form.get('email')
        usename.strip()

        email = form.get('email')
        email = email.strip()

        password = form.get('password')
        password = password.strip()

        address = form.get('address')
        address = address.strip()

        try:
            user = User.objects.create_user(usename, email)
            if user is not None:
                user.set_password(password)
                user.first_name = first_name
                user.address = address
                user.save()
                id = user.id
                msg = 'User registration successfully.'
        except Exception as e:
            msg = 'Something went wrong.'
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
        user = authenticate(request, username=username, password=password)
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


def logout_account(request):
    logout(request)
    return redirect('/accounts/login/')


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
        email = form.get('email')
        message = form.get('message')
        status = 0
        try:
            q_obj = UserQuery.objects.create(name=name,
                                             email=email,
                                             message=message,
                                             )
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
