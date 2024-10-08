from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


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
