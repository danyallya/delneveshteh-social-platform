# -*- coding:utf-8 -*-
from captcha.fields import CaptchaField, CaptchaTextInput

from django import forms

from account.models import Profile
from utils.forms import BaseForm

__author__ = 'M.Y'


class SignUpFormNoCaptcha(BaseForm):
    has_provider = False

    class Meta:
        model = Profile
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpFormNoCaptcha, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(required=True, label=u"رمز عبور", widget=forms.PasswordInput)
        # self.fields['re_password'] = forms.CharField(required=True, label=u"تکرار رمز عبور", widget=forms.PasswordInput)
        self.fields.keyOrder = ['email', 'username', 'password']

    def clean(self):
        cd = super(SignUpFormNoCaptcha, self).clean()
        email = cd.get('email')
        username = cd.get('username')
        try:
            Profile.objects.get(username=username)
            self.errors['username'] = self.error_class([u'نام کاربری تکراری می باشد.'])
        except Profile.DoesNotExist:
            pass
        try:
            Profile.objects.get(email=email)
            self.errors['email'] = self.error_class([u'پست الکترونیک تکراری می باشد.'])
        except Profile.DoesNotExist:
            pass
        return cd

    def save(self, commit=True):
        obj = super(SignUpFormNoCaptcha, self).save(commit=False)
        password = self.cleaned_data.get('password')
        obj.set_password(password)
        obj.save()
        return obj


class SignUpForm(SignUpFormNoCaptcha):
    captcha = CaptchaField(label=u"کد امنیتی", error_messages={
        'invalid': u"کد امنیتی وارد شده صحیح نمی باشد."}, widget=CaptchaTextInput(attrs={'placeholder': u"کد امنیتی"}))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.provide_fields()
        self.fields.keyOrder = ['email', 'username', 'password', 're_password', 'first_name', 'captcha']


class ForgetForm(forms.Form):
    email = forms.EmailField(label=u"پست الکترونیک",
                             widget=forms.TextInput(
                                 {'placeholder': u'پست الکترونیک', 'class': 'input left-align'}))
    captcha = CaptchaField(label=u"کد امنیتی", error_messages={
        'invalid': u"کد امنیتی وارد شده صحیح نمی باشد."},
                           widget=CaptchaTextInput(attrs={'placeholder': u"کد امنیتی", 'class': 'input left-align'}))

    def clean(self):
        cd = super(ForgetForm, self).clean()
        email = cd.get('email')
        if email:
            if not Profile.objects.filter(email=email).exists():
                self.errors['email'] = self.error_class([u'کاربری با این پست الکترونیک وجود ندارد.'])
        return cd


class ProfileForm(BaseForm):
    class Meta:
        model = Profile
        fields = ['email', 'username', 'first_name']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(required=False, label=u"رمز عبور جدید (در صورت تغییر)",
                                                  widget=forms.PasswordInput)
        self.fields['re_password'] = forms.CharField(required=False, label=u"تکرار رمز عبور",
                                                     widget=forms.PasswordInput)
        self.provide_fields()
        self.fields.keyOrder = ['email', 'username', 'password', 're_password', 'first_name']

    def clean(self):
        cd = super(ProfileForm, self).clean()
        email = cd.get('email')
        username = cd.get('username')
        password = cd.get('password')
        re_password = cd.get('re_password')
        if (password or re_password) and password != re_password:
            self.errors['password'] = self.error_class([u'رمز عبور با تکرار آن مطابقت ندارد.'])
        try:
            Profile.objects.exclude(id=self.instance.user.id).get(email=email)
            self.errors['email'] = self.error_class([u'پست الکترونیک تکراری می باشد.'])
        except Profile.DoesNotExist:
            pass
        try:
            Profile.objects.exclude(id=self.instance.user.id).get(username=username)
            self.errors['username'] = self.error_class([u'نام کاربری تکراری می باشد.'])
        except Profile.DoesNotExist:
            pass

        return cd

    def save(self, commit=True):
        obj = super(ProfileForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            obj.set_password(password)
        obj.save()
        return obj
