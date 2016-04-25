# from django.http.response import JsonResponse
import json
import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# from django.http.response import JsonResponse
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from account.forms import reserve_words
from account.models import Profile
from utils.forms import BaseForm
from utils.messages import MessageServices
from utils.persian import arToPersianChar


@never_cache
def logout(request):
    from django.contrib.auth import logout

    next_page = request.GET.get('next', '/')

    if 'change_pass' in next_page:
        next_page = '/'

    logout(request)
    return HttpResponseRedirect(next_page)


def login(request):
    from django.contrib.auth import authenticate, login

    next_page = request.GET.get('next', '/')

    if request.method == 'POST':

        username = arToPersianChar(request.POST.get('username'))
        password = request.POST.get('password')
        next_post = request.POST.get('next')
        if next_post:
            next_page = next_post
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
        else:
            login(request, user)

    context = {
        'app_path': request.get_full_path(),
        'next': request.get_full_path(),
    }

    if 'change_pass' in next_page:
        next_page = '/'

    if next_page:
        return HttpResponseRedirect(next_page)


def check(request):
    from django.contrib.auth import authenticate

    username = arToPersianChar(request.POST.get('username'))
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is None or not user.is_active:
        res = False
    else:
        res = True
    return HttpResponse(json.dumps(res), 'application/json')


def check_signup(request):
    username = arToPersianChar(request.POST.get('username'))

    res = True

    for item in reserve_words:
        if username in item:
            res = False

    if Profile.objects.filter(username=username):
        res = False
    return HttpResponse(json.dumps(res), 'application/json')


class SignUpForm(BaseForm):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'email', 'password')


def signup(request):
    from django.contrib.auth import authenticate, login

    next_page = request.GET.get('next', '/')

    if request.method == 'POST':
        username = arToPersianChar(request.POST.get('username'))
        email = arToPersianChar(request.POST.get('email', ''))
        password = request.POST.get('password')

        next_post = request.POST.get('next')
        if next_post:
            next_page = next_post

        if username and password:

            profile = Profile.objects.create(first_name=username, email=email, username=username)

            try:
                profile.set_password(password)
                profile.save()

                user = authenticate(username=profile.username, password=password)
                login(request, user)
                messages.success(request, "ثبت نام شما با موفقیت انجام شد.")
            except:
                pass

    return HttpResponseRedirect(next_page)


def forget(request):
    message = ""
    success = False
    if request.method == 'POST':
        email = arToPersianChar(request.POST.get('email'))
        if email and Profile.objects.filter(email=email).exists():
            MessageServices(email).start()
            message = u"رمز عبور به ایمیل شما ارسال خواهد شد."
            success = True
        else:
            message = "چنین ایمیلی پیدا نشد!"
            success = False

    res = {'s': success, 'm': message}
    return HttpResponse(json.dumps(res), 'application/json')


def change_pass(request):
    code = request.GET.get('c')
    if not code:
        raise Http404
    user = get_object_or_404(Profile, code=code)
    message = ""
    success = False
    if request.method == 'POST':
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if not password:
            message = "رمز عبور جدید را وارد نمایید."
        if password != repassword:
            message = "رمز عبور با تکرار آن مطابقت ندارد."

        if password and password == repassword:
            # new_pass = Profile.objects.make_random_password(10, string.ascii_lowercase)
            user.set_password(password)
            user.save()
            success = True
            message = "رمز عبور با موفقیت تغییر یافت. اکنون می توانید وارد شوید."
    return render(request, 'account/change_pass.html', {'message': message, 'success': success})


@login_required
def change_pass_ajax(request):
    message = ""
    success = False
    if request.method == 'POST':
        current_pass = request.POST.get('current_pass')
        new_pass = request.POST.get('new_pass')
        renew_pass = request.POST.get('renew_pass')

        if not new_pass:
            message = "رمز عبور جدید را وارد نمایید."

        if new_pass != renew_pass:
            message = "رمز عبور با تکرار آن مطابقت ندارد."

        check_pass = request.user.check_password(current_pass)
        if not check_pass:
            message = "رمز عبور فعلی شما نادرست است."

        if check_pass and new_pass and new_pass == renew_pass:
            # new_pass = Profile.objects.make_random_password(10, string.ascii_lowercase)
            request.user.set_password(new_pass)
            request.user.save()
            success = True
            message = "رمز عبور با موفقیت تغییر یافت."
    res = {'s': success, 'm': message}
    return HttpResponse(json.dumps(res), 'application/json')
