from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import DemoClass, MainUserDemo, AddUserDemoCode

# Create your views here.
from courses.models import Course
from .models import UserDemoClass


@login_required(login_url='/accounts/login/')
def demo_list(request):
    user_id = request.session.get('user_id')
    course = Course.objects.all().order_by('-id')
    context = {
        'course': course
    }
    return render(request, 'demo_list.html', context)


@login_required(login_url='/accounts/login/')
def demo_details(request, course_id):
    user_id = request.session.get('user_id')
    demo_class = DemoClass.objects.filter(course_id=course_id)
    context = {
        'demo_class': demo_class
    }
    return render(request, 'demo_details.html', context)


@login_required(login_url='/accounts/login/')
def count_video_play(request):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        status = 0
        try:
            AddUserDemoCode.objects.filter(user_id=user_id).update(code='')
            MainUserDemo.objects.filter(user_id=user_id).update(code='')
            status = 1
        except:
            status = status

        context = {
            'status': status
        }
        return JsonResponse(context)
