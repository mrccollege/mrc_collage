from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from numpy.core.defchararray import strip

from .models import DemoClass, MainUserDemo, AddUserDemoCode, BulkCode, UploadDemo

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
        bulk_code = form.get('bulk_code')
        status = 0
        try:
            bulk_code = UploadDemo.objects.filter(code__iexact=bulk_code)
            if bulk_code:
                bulk_code = bulk_code[0].code
                if bulk_code:
                    is_added = MainUserDemo.objects.filter(user_id=user_id, code=bulk_code).exists()
                    if is_added:
                        status = status
                    else:
                        obj = MainUserDemo.objects.create(user_id=user_id, code=bulk_code)
                        if obj:
                            status = 1
        except:
            status = status

        context = {
            'status': status
        }
        return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def get_demo_data(request):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        bulk_code = strip(form.get('bulk_code'))
        status = 0
        demo_class = UploadDemo.objects.filter(code__iexact=bulk_code).first()
        if demo_class:
            demo_data = {
                'title': demo_class.title,
                'description': demo_class.description,
                'file_url': demo_class.file.url if demo_class.file else None,
            }
        else:
            demo_data = None

        try:
            bulk_code = UploadDemo.objects.filter(code__iexact=bulk_code)
            if bulk_code:
                bulk_code = bulk_code[0].code
                if bulk_code:
                    is_added = MainUserDemo.objects.filter(user_id=user_id, code=bulk_code).exists()
                    if is_added:
                        status = status
                    else:
                        status = 1
        except:
            status = status

        context = {
            'status': status,
            'demo_data': demo_data,
        }
        return JsonResponse(context)
