from django.shortcuts import render
from .models import UserDemoCourse, DemoClass


# Create your views here.
def demo_list(request):
    user_id = request.session.get('user_id')
    course = UserDemoCourse.objects.filter(user_id=user_id).order_by('-id')
    context = {
        'course': course
    }
    return render(request, 'demo_list.html', context)


def demo_details(request, course_id):
    user_id = request.session.get('user_id')
    demo_class = DemoClass.objects.filter(course_id=course_id)
    context = {
        'demo_class': demo_class
    }
    return render(request, 'demo_details.html', context)
