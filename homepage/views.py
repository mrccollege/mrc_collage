import razorpay
from courses.models import CoursePurchased, Course, VideoFiles, UserWatch, CourseMaster, MonthMoney
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from homepage.models import Lookup


def homepage(request, id=0):
    if id != 0:
        course_master = Course.objects.filter(course_master_id=id)
    else:
        course_master = CourseMaster.objects.all()
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''
    context = {'id': id, 'course_master': course_master, 'home_banner': home_banner}
    return render(request, 'homepage.html', context)


@login_required(login_url='/accounts/login/')
def cart_page(request, id):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''

    user_id = request.session.get('user_id')
    course = Course.objects.get(id=id)
    # course_id = course.id
    # amount = course.totalprice
    # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    #
    # payment = client.order.create({'amount': int(amount) * 100, 'currency': 'INR', 'payment_capture': '1'})
    #
    # order_id = payment['id']
    # if user_id is not None:
    #     same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
    #     if same_user:
    #         CoursePurchased.objects.filter(user_id=user_id).update(razorpay_order_id=order_id)
    #     else:
    #         CoursePurchased.objects.create(user_id=user_id, razorpay_order_id=order_id, course_id=course_id)
    # else:
    #     return redirect('/accounts/login/')
    # context = {'payment': payment, 'course': course, 'home_banner': home_banner }
    context = {'course': course, 'home_banner': home_banner }
    return render(request, 'cart_page.html', context)


def month_amount(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        monts = MonthMoney.objects.filter(course_id=course_id)
        course_month = []
        for i in monts:
            data_dict = {}
            data_dict['id'] = i.id
            data_dict['month'] = i.month
            data_dict['money'] = i.money

            course_month.append(data_dict)

        context = {
            'monts': course_month,
        }
        return JsonResponse(context)

def get_change_month(request):
    user_id = request.session.get('user_id')
    course_id = request.GET.get('course_id')
    money = request.GET.get('money')
    print(money, '===================money')
    amount = money

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    payment = client.order.create({'amount': int(amount) * 100, 'currency': 'INR', 'payment_capture': '1'})

    order_id = payment['id']
    if user_id is not None:
        same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
        if same_user:
            CoursePurchased.objects.filter(user_id=user_id).update(razorpay_order_id=order_id)
        else:
            CoursePurchased.objects.create(user_id=user_id, razorpay_order_id=order_id, course_id=course_id)
    else:
        return redirect('/accounts/login/')
    context = {'payment': payment, 'order_id': order_id}
    return JsonResponse(context)


def success(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        form = request.GET
        razorpay_order_id = form.get('razorpay_order_id', None)
        razorpay_payment_id = form.get('razorpay_payment_id', None)
        razorpay_signature = form.get('razorpay_signature', None)
        course_id = form.get('course_id', None)
        price = form.get('price', None)
        discount = form.get('discount', None)
        totalprice = form.get('totalprice', None)
        quantity = form.get('quantity', None)
        payment_status = form.get('payment_status', None)
        try:
            course_obj = CoursePurchased.objects.filter(user_id=user_id, razorpay_order_id=razorpay_order_id).update(
                course_id=course_id, price=price, discount=discount, totalprice=totalprice, quantity=quantity,
                razorpay_payment_id=razorpay_payment_id, razorpay_signature=razorpay_signature,
                payment_status=payment_status, )
        except Exception as e:
            print(e, '=====================error in payment success function')

        if course_obj:
            msg = 'success'
        else:
            msg = 'failed'

        json_data = {'msg': msg}

        return JsonResponse(json_data)


def my_courses(request):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''
    user_id = request.session.get('user_id')
    if user_id is not None:
        course_purchased = CoursePurchased.objects.filter(user_id=user_id, payment_status='success').values_list(
            'course', flat=True)
        my_pur_cours = Course.objects.filter(id__in=course_purchased)
        context = {'my_course': my_pur_cours, 'home_banner': home_banner}
        return render(request, 'my_course.html', context)
    else:
        return redirect('/accounts/login/')


def watch_video(request, pre_next='', type='', course_id=0, file_id=0):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''
    user_id = request.session.get('user_id')
    type = type
    course_id = course_id
    file_type = ''
    try:
        thumb = Lookup.objects.get(code='common thumb')
    except:
        thumb = ''

    if user_id is not None:
        if type == 'professional':
            video_files = VideoFiles.objects.filter(course_id=course_id)
            context = {'type': type,
                       'data': video_files,
                       'thumb': thumb
                       }
            return render(request, 'professional_course.html', context)
        elif type == 'regular':
            video_files = VideoFiles.objects.filter(course_id=course_id)
            context = {'type': type,
                       'data': video_files,
                       'thumb': thumb,
                       }
            return render(request, 'regular.html', context)
        else:

            watch_video_ids = UserWatch.objects.filter(user_id=user_id, status='complete',
                                                       course_id=course_id).values_list('videofile', flat=True)
            if watch_video_ids:
                if file_id != 0:
                    if pre_next == 'pre':
                        video_path = VideoFiles.objects.filter(course_id=course_id, id__lt=file_id)[0]
                        if video_path:
                            file_id = video_path.id
                            file_type = video_path.file_type.file_type
                    else:
                        if pre_next == 'next':
                            video_path = VideoFiles.objects.filter(course_id=course_id, id__gt=file_id)[0]
                            if video_path:
                                file_id = video_path.id
                                file_type = video_path.file_type.file_type
                else:
                    try:
                        video_path = VideoFiles.objects.filter(course_id=course_id).exclude(id__in=watch_video_ids)[0]
                        file_id = video_path.id
                        file_type = video_path.file_type.file_type
                    except:
                        file_id= 0
                        video_path = ''
            else:
                try:
                    video_path = VideoFiles.objects.filter(course_id=course_id)[0]
                    file_id = video_path.id
                    file_type = video_path.file_type.file_type
                except:
                    file_id = 0
                    video_path = ''
            context = {'pre_next': pre_next, 'data': video_path, 'file_type': file_type, 'course_id': course_id, 'home_banner': home_banner, 'file_id': file_id}
            return render(request, 'common.html', context)
    else:
        redirect('/accounts/login/')


def count_video(request, id):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        if user_id is not None:
            count = int(form.get('count', None))
            video_id = id
            watch_obj = ''
            status = ''
            msg = ''
            try:
                video_obj = VideoFiles.objects.get(id=video_id)
                course = Course.objects.get(name__iexact=video_obj.course)
                course_id = course.id
                already_watch = UserWatch.objects.filter(user_id=user_id, course_id=course_id, videofile_id=video_id)
                if already_watch:
                    for already_watch in already_watch:
                        pre_count = already_watch.whatch_count
                        already_watch.whatch_count = count + pre_count
                        already_watch.status = 'complete'
                        already_watch.save()
                        status = 1
                else:
                    watch_obj = UserWatch.objects.create(user_id=user_id, course_id=course_id, videofile_id=video_id,
                                                         whatch_count=count, status='incomplete', )
                    if watch_obj:
                        msg = 'user watched video successfully'
                        status = 1
            except Exception as e:
                print(e, '=====================error in count_video function')
                msg = 'user not watched video successfully'

            json_data = {'msg': msg, 'status': status}
            return JsonResponse(json_data)
        return redirect('/accounts/login/')


def round_view(request, video_id):
    form = request.GET
    user_id = request.session.get('user_id')
    count = int(form.get('count', None))

    video_obj = VideoFiles.objects.get(id=video_id)
    course = Course.objects.get(name__iexact=video_obj.course)
    course_id = course.id

    status = ''
    msg = ''
    user_watch_video = ''

    try:
        user_watch_video = UserWatch.objects.get(user_id=user_id, videofile_id=video_id)
    except Exception as e:
        print(e, '=================e=================')

    if user_watch_video:
        whatch_count = user_watch_video.whatch_count
        round_view = video_obj.round_view
        if round_view > whatch_count:
            user_watch_video.whatch_count = int(whatch_count) + count
            user_watch_video.save()
            status = 1
            msg = 'Updated user_watched entry'

    else:
        watch_obj = UserWatch.objects.create(user_id=user_id, course_id=course_id, videofile_id=video_id,
                                                         whatch_count=count, status='incomplete', )
        if watch_obj:
            status = 0
            msg = 'Created user_watched entry'

    context = {
        'status': status,
        'msg': msg,
    }
    return JsonResponse(context)

