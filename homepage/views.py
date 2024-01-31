import datetime

import razorpay
from courses.models import CoursePurchased, Course, VideoFiles, UserWatch, CourseMaster, MonthMoney, FileType
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
import hashlib
from homepage.models import Lookup, CouponCode
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


def my_courses(request):
    try:
        home_banner = Lookup.objects.get(code='home_banner')
    except:
        home_banner = ''
    user_id = request.session.get('user_id')
    if user_id is not None:
        is_admin = User.objects.filter(id=user_id, username='admin')
        if is_admin:
            query = Q()
        else:
            course_purchased = CoursePurchased.objects.filter(user_id=user_id, payment_status='success').values_list(
                'course', flat=True)
            query = Q(id__in=course_purchased)
        my_pur_cours = Course.objects.filter(query)
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
        pro_count = 0
        try:
            for i in range(len(video)):
                # pro_count = VideoFiles.objects.filter(course_id=4).count()
                pro_count += 1
                new_product = VideoFiles.objects.create(file_type_id=file_type,
                                                        course_id=course,
                                                        day=pro_count,
                                                        title=video[i],
                                                        file=video[i],
                                                        # code_no=pro_count,
                                                        )
                # if new_product:
                # video_detail_url = request.build_absolute_uri(reverse('video_detail', args=[pro_count]))
                #
                # qr = qrcode.QRCode(version=1,
                #                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                #                    box_size=10,
                #                    border=4,
                #                    )
                # qr.add_data(video_detail_url)
                # qr.make(fit=True)
                #
                # img = qr.make_image(fill_color="black", back_color="white")
                #
                # qr_codes_dir = os.path.join(BASE_DIR, 'media', 'qr_codes')
                # os.makedirs(qr_codes_dir, exist_ok=True)
                #
                # qr_code_path = f"qr_codes/video_{pro_count}.png"
                # img.save(os.path.join(BASE_DIR, 'media', qr_code_path))
                #
                # new_product.qr_code = qr_code_path
                # new_product.save()
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
            video_dict['file_type'] = i.file_type.file_type
            video_dict['course'] = i.course.name
            video_dict['day'] = i.day if i.day else ''
            video_dict['title'] = i.title if i.title else ''
            video_dict['code_no'] = i.code_no if i.code_no else ''
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


@login_required(login_url='/accounts/login/')
def buy_course_detail(request, course_id):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        form = request.POST
        course_price = form.get('price')
        totalprice = form.get('totalprice')
        totalprice = round(totalprice, 1)
        discount = form.get('discount')
        month = form.get('month')
        course_id = form.get('course_id')

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({'amount': totalprice * 100, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment['id']

        same_user = CoursePurchased.objects.filter(user_id=user_id, course_id=course_id)
        if same_user:
            CoursePurchased.objects.filter(user_id=user_id).update(razorpay_order_id=order_id)
        else:
            CoursePurchased.objects.create(user_id=user_id, razorpay_order_id=order_id, course_id=course_id)

        context = {
            'payment': payment,
            'course_price': course_price,
            'totalprice': totalprice,
            'discount': discount,
            'month': month,
            'course_id': course_id,
            'razorkey': settings.RAZOR_KEY_ID,
        }
        return render(request, 'final_pay.html', context)

    else:
        course_data = Course.objects.get(id=course_id)

        already_purchased = CoursePurchased.objects.filter(course_id=course_id, user_id=user_id,
                                                           payment_status='success')
        if already_purchased:
            return redirect('/')

        try:
            loader_img = Lookup.objects.get(code='loader_img')
            loader_img = loader_img.file.url
        except:
            loader_img = ''

        context = {
            'course_data': course_data,
            'loader_img': loader_img,
        }
        return render(request, 'new_cart_page.html', context)


def payment_success(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        course_obj = ''
        form = request.GET
        razorpay_order_id = form.get('razorpay_order_id', None)
        razorpay_payment_id = form.get('razorpay_payment_id', None)
        razorpay_signature = form.get('razorpay_signature', None)
        course_id = form.get('course_id', None)
        price = form.get('course_price', None)
        discount = form.get('discount', None)
        totalprice = form.get('totalprice', None)
        quantity = form.get('quantity', None)
        payment_status = form.get('payment_status', None)
        month = int(form.get('month', 0))
        status = 0
        from datetime import datetime, timedelta

        def calculate_future_date(month):
            current_date = datetime.now()
            future_date = current_date + timedelta(days=30 * month)  # Assuming a month has 30 days for simplicity
            return future_date

        future_date = calculate_future_date(month)
        try:
            query = Q(user_id=user_id, razorpay_order_id=razorpay_order_id)
            course_obj = CoursePurchased.objects.filter(query).update(course_id=course_id,
                                                                      price=price,
                                                                      discount=discount,
                                                                      totalprice=totalprice,
                                                                      quantity=quantity,
                                                                      razorpay_payment_id=razorpay_payment_id,
                                                                      razorpay_signature=razorpay_signature,
                                                                      payment_status=payment_status,
                                                                      end_date=future_date,
                                                                      month=month)
            if course_obj:
                status = 1
        except Exception as e:
            print(e, '=====error in payment success function')
            status = 0
        json_data = {'status': status}

        return JsonResponse(json_data)


def get_service_month(request):
    if request.method == 'GET':
        form = request.GET
        course_id = form.get('course_id')
        price_data = MonthMoney.objects.filter(course_id=course_id).order_by('month')
        data_list = []
        if price_data:
            for i in price_data:
                data_dict = {}
                data_dict['id'] = i.id
                data_dict['month'] = i.month
                data_dict['price'] = i.money
                data_list.append(data_dict)

        context = {
            'data': data_list
        }
        return JsonResponse(context)


def get_service_price(request):
    if request.method == 'GET':
        form = request.GET
        course_id = form.get('course_id')
        month_id = form.get('month_id')
        data_dict = {}
        price_data = MonthMoney.objects.get(id=month_id)

        data_dict['month'] = price_data.month
        data_dict['price'] = price_data.money

        context = {
            'data': data_dict,
            'course_id': course_id
        }
        return JsonResponse(context)


@login_required(login_url='/accounts/login/')
def apply_coupon_code(request):
    if request.method == 'GET':
        form = request.GET
        coupon_code = form.get('coupon_code')
        coupon_data = CouponCode.objects.filter(coupon_code__exact=coupon_code)
        coupon_dict = {}
        if coupon_data:
            coupon_dict['percent'] = coupon_data[0].percent
        context = {
            'coupon_data': coupon_dict
        }
        return JsonResponse(context)
