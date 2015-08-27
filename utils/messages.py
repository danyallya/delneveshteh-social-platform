# -*- coding:utf-8 -*-
import threading
import urllib
from django.conf import settings

from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives


__author__ = 'M.Y'


class MessageServices(threading.Thread):
    from_email = u'fanoos.ir@gmail.com'
    admin_email = u'fanoos.ir@gmail.com'

    @staticmethod
    def send_forget_password(email):
        try:
            user = User.objects.get(email=email)
            user.profile.create_code()

            url = settings.SITE_URL + "/change_pass/?c=" + urllib.quote(user.profile.code)
            message = u"""
                <div style="direction:rtl;font-family:tahoma;font-size:17px;">
                باسلام
                <br/>
شما درخواست فراموشی گذرواژه را ارسال کرده اید.
    <br/>
    با استفاده از لینک زیر می توانید گذرواژه جدید خود را دریافت نمایید.
                    <br/><br/>
                    <br/>
                    <a href="%s">%s</a>

                    <br/>
                    <br/>
                    <br/>
                    موفق باشید
                </div>
                """ % (url, url)
            msg = EmailMultiAlternatives(subject=u"تغییر گذرواژه در فانوس", body='',
                                         from_email=MessageServices.from_email,
                                         to=[user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()
        except Exception as s:
            print(s)
