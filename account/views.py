from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
# from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from account.models import Profile
from post.models import Movie


@never_cache
def logout(request):
    from django.contrib.auth import logout

    logout(request)
    return HttpResponseRedirect(reverse('home'))


def login(request):
    from django.contrib.auth import authenticate, login

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
        else:
            login(request, user)
            next_page = request.GET.get('next', '/')
            if next_page:
                return HttpResponseRedirect(next_page)

    context = {
        'app_path': request.get_full_path(),
        'next': request.get_full_path(),
    }

    return render(request, 'account/login.html', context)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'email', 'password')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST.copy())
        if form.is_valid():
            profile = form.save()
            password = form.cleaned_data.get('password')
            profile.set_password(password)
            profile.save()
            messages.success(request, u"ثبت نام شما با موفقیت انجام شد. اکنون می توانید وارد شوید.")
            # next_page = request.GET.get('next') or '/'

            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignUpForm()
    return render(request, 'registerForm.html', {'form': form})


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'email')


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST.copy(), request.FILES.copy(), instance=request.user)
        if form.is_valid():
            profile = form.save()
            password = request.POST.get('password')
            if password:
                profile.set_password(password)
                profile.save()
            messages.success(request, u"ثبت نام شما با موفقیت انجام شد. اکنون می توانید وارد شوید.")
            # next_page = request.GET.get('next') or '/'

            return HttpResponseRedirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'editProfile.html',
                  {'form': form, 'profile': request.user, 'birth_date': request.user.standard_birth})


def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, u"رمز عبور به پست الکترونیک شما ارسال خواهد شد.")
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.success(request, u"لطفا پست الکترونیک خود را وارد نمایید.")
    return render(request, 'forgetPass.html', {})


@login_required(login_url='login')
def search(request):
    q = request.GET.get('q', '').strip()
    users = Profile.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q)).exclude(id=request.user.id)
    movies = Movie.get_search_res(q)
    return render(request, 'searchResult.html', {'users': users, 'movies': movies})


@login_required
def search_ajax(request):
    q = request.GET.get('q', '').strip()
    users = Profile.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q)).exclude(id=request.user.id)
    user_res = []
    for user in users:
        user_res.append({
            "title": user.name,
            "url": reverse("show_profile", kwargs={'profile_username': user.username}),
            "image": user.profile_image,
        })
    movies = Movie.get_search_res(q)
    movie_res = []
    for movie in movies:
        movie_res.append({
            "title": movie.name,
            "url": reverse("movie_page", kwargs={'movie_id': movie.id}),
            "image": movie.movie_image,
        })
    res = {
        "results": {
            "category1": {
                "name": "کاربران",
                "results": user_res
            },
            "category2": {
                "name": "فیلم ها",
                "results": movie_res
            }
        },
        "action": {
            "url": reverse("search") + "?q=" + q,
            "text": "مشاهده همه نتایج",
        },
    }
    return JsonResponse(res)
