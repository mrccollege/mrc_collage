from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import DemoClass

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
        file_id = form.get('file_id')
        status = 0
        demo_class = UserDemoClass.objects.filter(user_id=user_id, file_id=file_id)
        if demo_class:
            play_again = UserDemoClass.objects.filter(user_id=user_id, file_id=file_id, watch_count=0)
            if play_again:
                UserDemoClass.objects.filter(user_id=user_id, file_id=file_id).update(watch_count=1)
                status = 1
            else:
                status = status
        else:
            demo_class = UserDemoClass.objects.create(user_id=user_id,
                                                      file_id=file_id,
                                                      watch_count=1
                                                      )
            if demo_class:
                status = 1

        context = {
            'status': status
        }
        return JsonResponse(context)
