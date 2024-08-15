from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course, VideoFiles
from django.contrib.auth.models import User
from courses.models import CoursePurchased, Course, VideoFiles, UserWatch, CourseMaster, MonthMoney, FileType
from django.db.models import Q
from django.shortcuts import render, redirect


@csrf_exempt
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        course_list = []
        for i in courses:
            data_dict = {}
            data_dict['id'] = i.id
            data_dict['name'] = i.name if i.name else ''
            data_dict['instructor'] = i.instructor if i.instructor else ''
            data_dict['description'] = i.description if i.description else ''
            data_dict['course_image'] = request.build_absolute_uri(i.course_image.url) if i.course_image else ''
            data_dict['demo_video'] = request.build_absolute_uri(i.demo_video) if str(i.demo_video) else ''
            data_dict['created_at'] = i.created_at if i.created_at else ''
            data_dict['course_lang'] = i.course_lang if i.course_lang else ''
            course_list.append(data_dict)
        context = {
            'course_list': course_list
        }
        return JsonResponse(context)


@csrf_exempt
def course_detail(request):
    if request.method == 'GET':
        data = request.GET
        course_id = int(data.get('course_id'))
        courses = VideoFiles.objects.filter(course_id=course_id)
        course_details_list = []
        for i in courses:
            data_dict = {}
            data_dict['title'] = i.title
            data_dict['file_type'] = i.file_type.file_type
            data_dict['video'] = request.build_absolute_uri(i.file.url) if i.file else ''

            course_details_list.append(data_dict)
        context = {
            'course_details': course_details_list
        }
        return JsonResponse(context)


@csrf_exempt
def my_courses(request):
    if request.method == 'GET':
        data = request.GET
        user_id = int(data.get('user_id'))
        is_admin = User.objects.filter(id=user_id, username='admin')
        if is_admin:
            query = Q()
        else:
            query = Q(user_id=user_id) & Q(payment_status='success') | Q(user_id=user_id) & Q(payment_status='renew')
            course_purchased = CoursePurchased.objects.filter(query).values_list('course', flat=True)
            query = Q(id__in=course_purchased)
        my_pur_cours = Course.objects.filter(query)
        course_list = []
        for i in my_pur_cours:
            data_dict = {}
            data_dict['id'] = i.id
            data_dict['name'] = i.name if i.name else ''
            data_dict['instructor'] = i.instructor if i.instructor else ''
            data_dict['description'] = i.description if i.description else ''
            data_dict['course_image'] = request.build_absolute_uri(i.course_image.url) if i.course_image else ''
            data_dict['demo_video'] = request.build_absolute_uri(i.demo_video) if str(i.demo_video) else ''
            data_dict['created_at'] = i.created_at if i.created_at else ''
            data_dict['course_lang'] = i.course_lang if i.course_lang else ''
            course_list.append(data_dict)
        context = {'my_course': course_list}
        return JsonResponse(context)
