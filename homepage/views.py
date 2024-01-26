import datetime

import razorpay
from courses.models import CoursePurchased, Course, VideoFiles, UserWatch, CourseMaster, MonthMoney, FileType
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
import hashlib
from homepage.models import Lookup
import os
import qrcode
from django.urls import reverse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def homepage(request, id=0):
    if id != 0:
        course_master = Course.objects.filter(course_master_id=id)
    else:
        course_master = CourseMaster.objects.all().order_by('-id')
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''

    context = {
        'id': id,
        'course_master': course_master,
        'home_banner': home_banner.file.url,
    }
    # return render(request, 'homepage.html', context)
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login/')
def cart_page(request, id, month=1):
    if month:
        month = month

    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''

    user_id = request.session.get('user_id')
    course = Course.objects.get(id=id)
    monts = ''
    amount = ''
    payment = ''
    order_id = ''
    already_purchased = ''
    if user_id is not None:
        try:
            already_purchased = CoursePurchased.objects.get(course_id=id, user_id=user_id, payment_status='success')
            if already_purchased:
                return redirect('/')
        except:
            pass

        try:
            monts = MonthMoney.objects.get(course_id=id, month=month)
            amount = monts.money
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            if amount:
                payment = client.order.create({'amount': int(amount) * 100, 'currency': 'INR', 'payment_capture': '1'})

                order_id = payment['id']
                same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=id)
                if same_user:
                    CoursePurchased.objects.filter(user_id=user_id).update(razorpay_order_id=order_id)
                else:
                    CoursePurchased.objects.create(user_id=user_id, razorpay_order_id=order_id, course_id=id)
        except Exception as e:
            print(e, '------e---------')

    else:
        return redirect('/accounts/login/')

    pay_amt = amount
    print(amount, '===================amount')
    context = {
        'id': id,
        'payment': payment,
        'order_id': order_id,
        'pay_amt': pay_amt,
        'course': course,
        'home_banner': home_banner,
        'month': month
    }

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
            'month': course_month,
        }
        return JsonResponse(context)


def success(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        course_obj = ''
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
        months = int(form.get('month', 0))

        from datetime import datetime, timedelta

        def calculate_future_date(months):
            current_date = datetime.now()
            future_date = current_date + timedelta(days=30 * months)  # Assuming a month has 30 days for simplicity
            return future_date

        future_date = calculate_future_date(months)
        try:
            course_obj = CoursePurchased.objects.filter(user_id=user_id, razorpay_order_id=razorpay_order_id).update(
                course_id=course_id, price=price, discount=discount, totalprice=totalprice, quantity=quantity,
                razorpay_payment_id=razorpay_payment_id, razorpay_signature=razorpay_signature,
                payment_status=payment_status, end_date=future_date)
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
                       'thumb': thumb,
                       'home_banner': home_banner,
                       }
            # return render(request, 'professional_course.html', context)
            return render(request, 'course-details.html', context)
        elif type == 'regular':
            video_files = VideoFiles.objects.filter(course_id=course_id)
            context = {'type': type,
                       'data': video_files,
                       'thumb': thumb,
                       'home_banner': home_banner,
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
                        file_id = 0
                        video_path = ''
            else:
                try:
                    video_path = VideoFiles.objects.filter(course_id=course_id)[0]
                    file_id = video_path.id
                    file_type = video_path.file_type.file_type
                except:
                    file_id = 0
                    video_path = ''
            context = {'pre_next': pre_next, 'data': video_path, 'file_type': file_type, 'course_id': course_id,
                       'home_banner': home_banner, 'file_id': file_id}
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


def add_course(request):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''

    try:
        loader_img = Lookup.objects.get(code='loader_img')
        loader_img = loader_img.file.url
    except:
        loader_img = ''

    file_type = FileType.objects.all()
    course = Course.objects.all()

    context = {
        'home_banner': home_banner,
        'file_type': file_type,
        'course': course,
        'loader_img': loader_img,
    }
    return render(request, 'add_course.html', context)


def upload_video(request):
    if request.method == 'POST':
        form = request.POST
        form1 = request.FILES
        file_type = form.get('file_type')
        course = form.get('courseName')
        video = form1.getlist('videoFile')
        try:
            for i in range(len(video)):
                pro_count = VideoFiles.objects.filter(course_id=4).count()
                pro_count = pro_count + 1
                new_product = VideoFiles.objects.create(file_type_id=file_type,
                                                        course_id=course,
                                                        day=pro_count,
                                                        title=video[i],
                                                        file=video[i],
                                                        code_no=pro_count,
                                                        )
                if new_product:
                    video_detail_url = request.build_absolute_uri(reverse('video_detail', args=[pro_count]))

                    qr = qrcode.QRCode(version=1,
                                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                                       box_size=10,
                                       border=4,
                                       )
                    qr.add_data(video_detail_url)
                    qr.make(fit=True)

                    img = qr.make_image(fill_color="black", back_color="white")

                    qr_codes_dir = os.path.join(BASE_DIR, 'media', 'qr_codes')
                    os.makedirs(qr_codes_dir, exist_ok=True)

                    qr_code_path = f"qr_codes/video_{pro_count}.png"
                    img.save(os.path.join(BASE_DIR, 'media', qr_code_path))

                    new_product.qr_code = qr_code_path
                    new_product.save()
            status = 'success'
            msg = 'video files uploaded.'
        except Exception as e:
            msg = str(e)
            status = 'error'

    context = {
        'status': status,
        'msg': msg,
    }
    return JsonResponse(context)


def video_detail(request, id):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''
    video = VideoFiles.objects.get(code_no=id)
    context = {
        'home_banner': home_banner,
        'video': video,

    }
    return render(request, 'video_detail.html', context)


def view_list(request, course_id):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''
    context = {
        'home_banner': home_banner,
        'course_id': course_id,
    }
    return render(request, 'view_list_kshar_sutra.html', context)


def get_kshar_sutra_videos(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        video_list = []
        videos = VideoFiles.objects.filter(course_id=course_id)
        for i in videos:
            video_dict = {}
            video_dict['id'] = i.id
            video_dict['course'] = i.course.name
            video_dict['day'] = i.day
            video_dict['title'] = i.title
            video_dict['code_no'] = i.code_no
            video_dict['qr_code'] = i.qr_code.url
            video_list.append(video_dict)
        context = {
            'video_list': video_list
        }
        return JsonResponse(context)


def delete_files(request):
    video_id = request.GET.get('video_id')
    try:
        video = VideoFiles.objects.get(id=video_id)

        try:
            video_file_path = video.file.url
            video_file_path = os.path.join(BASE_DIR + video_file_path)
            if os.path.exists(video_file_path):
                os.remove(video_file_path)
        except Exception as e:
            print(e)

        try:
            qr_code_file_path = video.qr_code.url
            qr_code_file_path = os.path.join(BASE_DIR + qr_code_file_path)
            if os.path.exists(qr_code_file_path):
                os.remove(qr_code_file_path)
        except Exception as e:
            print(e)

        video.delete()

        status = 'success'
        msg = 'Deleted file.'
    except Exception as e:
        print(e)
        status = 'error'
        msg = 'No file deleted!'
    context = {
        'status': status,
        'msg': msg,
    }
    return JsonResponse(context)
