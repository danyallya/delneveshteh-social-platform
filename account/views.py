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
