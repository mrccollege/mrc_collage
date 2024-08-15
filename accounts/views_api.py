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
