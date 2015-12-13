import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from comment.models import Comment
from post.models import Post
from utils.models import BaseModel
from utils.templatetags.date_template_tags import pdate_if_date


class Profile(AbstractUser):
    # birth_date = models.DateField(verbose_name="تاریخ تولد", null=True)
    # image = models.ImageField(blank=True, null=True, upload_to='user_images/')

    last_act = models.DateTimeField(verbose_name="آخرین حضور", null=True, blank=True, auto_now=True)

    posts_count = models.IntegerField(verbose_name="تعداد پست ها", default=0)
    comments_count = models.IntegerField(verbose_name="تعداد نظرها", default=0, null=True)

    week_posts_count = models.IntegerField(verbose_name="تعداد پست های هفته", default=0)
    month_posts_count = models.IntegerField(verbose_name="تعداد پست های ماه", default=0)

    def __str__(self):
        return self.name

    # @property
    # def standard_birth(self):
    #     if self.birth_date:
    #         return self.birth_date.strftime("%Y-%m-%d")

    # @property
    # def age(self):
    #     if self.birth_date:
    #         return date.today().year - self.birth_date.year

    def update(self):
        today = datetime.date.today()

        week = today - datetime.timedelta(days=7)
        month = today - datetime.timedelta(days=30)

        self.comments_count = self.comment_set.count()
        self.posts_count = self.post_set.count()
        self.week_posts_count = self.post_set.filter(created_on__gt=week).count()
        self.month_posts_count = self.post_set.filter(created_on__gt=month).count()
        self.save()

    @property
    def name(self):
        return self.username

    def get_user_summery(self):
        res = {'u': self.username, 'p': Post.objects.filter(active=True, creator__username=self.username).count(),
               'c': Comment.objects.filter(active=True, user__username=self.username).count(),
               'da': pdate_if_date(self.date_joined), 'l': self.last_date, 'i': self.id}
        return res

    def get_android_fields(self):
        return {'u': self.username, 'e': self.email}
        # @property
        # def profile_image(self):
        #     if self.image:
        #         # print('%s%s' % (settings.MEDIA_URL, self.image))
        #         return '%s%s' % (settings.MEDIA_URL, self.image)
        #     else:
        #         return '/static/img/temp.jpg'

    @property
    def last_date(self):
        if not self.last_act:
            return "---"
        now = datetime.datetime.utcnow()
        sec = (now - self.last_act.replace(tzinfo=None)).total_seconds()
        if sec < 20:
            return " چند ثانیه قبل"
        elif sec < 60:
            return "%s ثانیه قبل" % int(sec)
        elif sec < 60 * 60:
            return "%s دقیقه قبل" % int(sec / 60)
        elif sec < 60 * 60 * 24:
            return "%s ساعت قبل" % int(sec / (60 * 60))
        elif sec < 60 * 60 * 24 * 7:
            return "%s روز قبل" % int(sec / (60 * 60 * 24))
        elif sec < 60 * 60 * 24 * 7 * 54:
            return "%s هفته قبل" % int(sec / (60 * 60 * 24 * 7))
        else:
            return pdate_if_date(self.last_act)

    @staticmethod
    def get_queryset_by_param(p):
        if p == 'week':
            return Profile.objects.order_by('-week_posts_count')[:20]
        elif p == 'month':
            return Profile.objects.order_by('-month_posts_count')[:20]
        elif p == 'all':
            return Profile.objects.order_by('-posts_count')[:20]


class Suggestion(BaseModel):
    SUGGESTION_TYPES = (
        (1, "پیشنهاد و انتقاد"),
        (2, "تبلیغات"),
        (3, "ثبت سفارش"),
    )
    sug_type = models.IntegerField(verbose_name="نوع", null=True, default=1, choices=SUGGESTION_TYPES)
    email = models.EmailField(verbose_name=u"ایمیل", null=True)
    body = models.TextField(verbose_name=u"متن", null=True, max_length=3000)
    phone = models.CharField(verbose_name=u"شماره تماس", null=True, max_length=100)

    class Meta:
        verbose_name = u"تماس با ما"
        verbose_name_plural = u"تماس با ما"

    def __str__(self):
        return self.name
