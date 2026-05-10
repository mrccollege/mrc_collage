from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course, VideoFiles
from django.contrib.auth.models import User
from courses.models import CoursePurchased, Course, VideoFiles, UserWatch, CourseMaster, MonthMoney, FileType, Category,  CourseMasterDisplay
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


@csrf_exempt
def home_catalog(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    categories = []
    main_categories = Category.objects.all().order_by("Category_main_id")

    for main_category in main_categories:
        screen_columns = CourseMaster.objects.filter(
            ScreenColumn_id=main_category.Category_main_id
        ).order_by("id")

        master_ids = list(screen_columns.values_list("id", flat=True))

        category_courses = Course.objects.filter(
            course_master_id__in=master_ids
        ).order_by("id")

        courses = []
        for course in category_courses:
            courses.append({
                "id": course.id,
                "course_name": course.name or "",
                "image": request.build_absolute_uri(course.course_image.url) if course.course_image else "",
            })

        if not courses:
            continue

        categories.append({
            "category_id": main_category.Category_main_id,
            "category_name": main_category.Category_main_name or "",
            "courses": courses,
        })

    return JsonResponse({"categories": categories})


@csrf_exempt
def course_full_detail(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    course_id = request.GET.get("course_id")
    if not course_id:
        return JsonResponse({"error": "course_id is required"}, status=400)

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)

    category_id = getattr(course, "course_master_id", None)
    category_name = ""

    if category_id:
        category = Category.objects.filter(Category_main_id=category_id).first()
        if category:
            category_name = category.Category_main_name or ""

    data = {
        "id": course.id,
        "category_id": category_id,
        "category_name": category_name,
        "course_name": course.name or "",
        "instructor": getattr(course, "instructor", "") or "",
        "description": getattr(course, "description", "") or "",
        "image": request.build_absolute_uri(course.course_image.url) if getattr(course, "course_image", None) else "",
        "demo_video": request.build_absolute_uri(course.demo_video.url) if getattr(course, "demo_video", None) else "",
        "language": getattr(course, "course_lang", "") or "",
        "type": getattr(course, "type", "") or "",
        "validate_for": getattr(course, "validate_for", None),
    }

    return JsonResponse(data)

@csrf_exempt
def home_catalog1(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    categories = []
    main_categories = Category.objects.all().order_by("Category_main_id")

    for main_category in main_categories:
        screen_columns = CourseMaster.objects.filter(
            ScreenColumn_id=main_category.Category_main_id
        ).order_by("id")

        master_ids = list(screen_columns.values_list("id", flat=True))

        category_courses = Course.objects.filter(
            course_master_id__in=master_ids
        ).order_by("id")

        courses = []
        for course in category_courses:
            # --- Fetching data from courses_coursemasterdisplay ---
            # We filter by course_master_id to get the display settings
            display_info = CourseMasterDisplay.objects.filter(
                course_master_id=course.id
            ).first()

            courses.append({
                "id": course.id,
                "course_name": course.name or "",
                "image": request.build_absolute_uri(course.course_image.url) if course.course_image else "",
                # --- New columns added below ---
                "screen_order": display_info.screen_order if display_info else 0,
                "rating": display_info.rating if display_info else 0.0,
             
            })

        if not courses:
            continue

        categories.append({
            "category_id": main_category.Category_main_id,
            "category_name": main_category.Category_main_name or "",
            "courses": courses,
        })

    return JsonResponse({"categories": categories})