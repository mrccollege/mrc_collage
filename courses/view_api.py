from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Course, VideoFiles


@csrf_exempt
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        course_list = []
        for i in courses:
            data_dict = {}
            data_dict['name'] = i.name if i.name else ''
            data_dict['instructor'] = i.instructor if i.instructor else ''
            data_dict['description'] = i.description if i.description else ''
            data_dict['course_image'] = str(i.course_image) if str(i.course_image) else ''
            data_dict['demo_video'] = str(i.demo_video) if str(i.demo_video) else ''
            data_dict['created_at'] = i.created_at if i.created_at else ''
            data_dict['course_lang'] = i.course_lang if i.course_lang else ''
            course_list.append(data_dict)
        context = {
            'course_list': course_list
        }
        return JsonResponse(context)


@csrf_exempt
def course_detail(request, id):
    if request.method == 'GET':
        courses = VideoFiles.objects.filter(course_id=id)
        course_details_list = []
        for i in courses:
            data_dict = {}
            data_dict['title'] = i.title
            data_dict['file'] = str(i.file)

            course_details_list.append(data_dict)
        context = {
            'course_details': course_details_list
        }
        return JsonResponse(context)
