from django.shortcuts import render


# Create your views here.
def demo_list(request):
    user_id = request.session.get('user_id')
    context = {
        'course': ''
    }
    return render(request, 'demo_list.html', context)


def demo_details(request, course_id):
    user_id = request.session.get('user_id')
    context = {
        'demo_class': ''
    }
    return render(request, 'demo_details.html', context)
