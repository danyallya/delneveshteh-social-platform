import datetime
import json

from colorful.fields import RGBColorField
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query_utils import Q

from django.utils.encoding import smart_text

from comment.handler import CommentHandler
from comment.models import Comment
from utils.calverter import gregorian_to_jalali
from utils.models import BaseModel
from utils.templatetags.date_template_tags import pdate_if_date


class PostImage(models.Model):
    image = models.ImageField(verbose_name=u"تصویر", upload_to="extra_images")
    movie = models.ForeignKey('Post', verbose_name="اثر", null=True, on_delete=models.CASCADE,
                              related_name='extra_images')

    class Meta:
        verbose_name = u"تصویر اثر"
        verbose_name_plural = u"تصاویر اثر"

    def __str__(self):
        return self.image.url

    @property
    def image_url(self):
        return settings.SITE_URL + self.image.url


class PostLike(models.Model):
    user = models.ForeignKey('account.Profile', verbose_name="کاربر")
    post = models.ForeignKey('post.Post', verbose_name="پست", related_name='likes')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "پسندیدن"
        verbose_name_plural = "پسندیدن  ها"
        # unique_together = (('user', 'post_id',),)

    def __str__(self):
        return u"%s likes %s" % (self.user, self.post)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(PostLike, self).save(force_insert, force_update, using, update_fields)
        self.post.update()

    def delete(self, using=None):
        post = self.post
        super(PostLike, self).delete(using)
        post.update()


class PostRate(models.Model):
    user = models.ForeignKey('account.Profile', verbose_name="کاربر")
    rate = models.IntegerField(verbose_name="امتیاز")
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "امتیاز کاربر"
        verbose_name_plural = "امتیاز کاربران"


class PostReport(models.Model):
    user = models.ForeignKey('account.Profile', verbose_name="کاربر", null=True, blank=True)
    post = models.ForeignKey('post.Post', verbose_name="پست")
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "گزارش پست"
        verbose_name_plural = "گزارش پست"

    def __str__(self):
        return str(self.post)


class Post(BaseModel):
    text = models.TextField()
    active = models.BooleanField(verbose_name="نمایش", default=True)

    color = RGBColorField(verbose_name="رنگ", default="#528c8a")

    rate = models.FloatField(verbose_name="امتیاز", default=0, null=True)
    comments_count = models.IntegerField(verbose_name="تعداد نظرها", default=0, null=True)

    like_count = models.IntegerField(verbose_name="پسندیدن", default=0)

    POST_TYPES = (
        (1, 'دلنوشته'),
        (2, 'بحث'),
        (3, 'مناسبت'),
        (4, 'حدیث'),
    )

    post_type = models.IntegerField(verbose_name="نوع", default=1, choices=POST_TYPES)

    is_spec = models.BooleanField(verbose_name="داغ", default=False)

    version_code = models.IntegerField(verbose_name="ورژن نرم افزار", default=1)

    android_version = models.IntegerField(verbose_name="ورژن اندروید", default=1)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        get_latest_by = 'created_on'

    def __str__(self):
        if len(self.text) > 31:
            return self.text[:30] + " ..."
        else:
            return self.text

    def update(self):
        self.like_count = self.likes.count()
        self.comments_count = Comment.objects.filter(
            content_type=PostContentType,
            object_pk=smart_text(self.id),
            active=True
        ).count()
        self.save()
        self.creator.update()

    def get_detail_json(self, user):
        data = self.get_summery_fields(user)

        comments = Comment.objects.filter(
            content_type=PostContentType,
            object_pk=smart_text(self.id),
            active=True
        )
        comments_json = CommentHandler(comments, user_id=user.id if user else None).render_comments_json()

        data.update({'cj': comments_json})

        return json.dumps(data)

    def get_comments(self):
        c_type = ContentType.objects.get_for_model(Post)
        comments = Comment.objects.filter(
            content_type=c_type,
            object_pk=smart_text(self.id),
            active=True
        )
        comments_dict = []
        for comment in comments:
            comments_dict.append(
                {'t': comment.user_name, 'c': comment.comment, 'd': gregorian_to_jalali(comment.submit_date)})
        return comments

    def get_extra_image_urls(self):
        res = []
        for image in self.extra_images.all():
            res.append(image.image_url)
        return res

    def is_fav(self, user):
        if user.is_anonymous():
            return False
        return PostLike.objects.filter(user=user, post_id=self.id).exists()

    def get_summery_fields(self, user):
        return {'d': self.id, 'n': self.creator.name if self.creator else "ناشناس", 'de': self.text, 'da': self.date,
                "lc": self.like_count, 'cc': self.comments_count, 'f': self.is_fav(user), 'co': self.color,
                'ty': self.get_post_type_display()}

    def get_old_summery_fields(self, user):
        text = self.text
        if self.version_code > 1:
            text += " <br/> این پست در نسخه جدید گذاشته شده است. لطفا نرم افزار خود را آپدیت نمایید."

        return {'d': self.id, 'n': self.creator.name if self.creator else "ناشناس", 'de': text, 'da': self.date,
                "lc": self.like_count, 'cc': self.comments_count, 'f': self.is_fav(user), 'co': self.color,
                'ty': self.get_post_type_display()}

    @staticmethod
    def get_old_summery_json(posts, user):
        data = []
        for post in posts:
            data.append(post.get_old_summery_fields(user))
        return json.dumps(data)

    @staticmethod
    def get_summery_json(posts, user):
        data = []
        for post in posts:
            data.append(post.get_summery_fields(user))
        return json.dumps(data)

    @property
    def date(self):
        now = datetime.datetime.utcnow()
        sec = (now - self.created_on.replace(tzinfo=None)).total_seconds()
        if sec < 60:
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
            return pdate_if_date(self.created_on)

    @staticmethod
    def get_queryset_by_param(p):
        posts = Post.objects.filter(active=True)
        if p == 'hot':
            posts = posts.filter(Q(is_spec=True) | Q(comments_count__gt=10) | Q(like_count__gt=10))
        elif p == 'del':
            posts = posts.filter(post_type=1)
        elif p == 'talk':
            posts = posts.filter(post_type=2)
        elif p == 'monasebat':
            posts = posts.filter(post_type=3)
        elif p == 'hadis':
            posts = posts.filter(post_type=4)
        else:
            posts = posts.none()
        return posts

    @staticmethod
    def get_post_type_by_param(p):
        if p == 'del':
            return 1
        elif p == 'talk':
            return 2
        elif p == 'monasebat':
            return 3
        elif p == 'hadis':
            return 4
        return None

    def get_page_json(self, user):
        data = self.get_summery_fields(user)

        comments = Comment.objects.filter(
            content_type=PostContentType,
            object_pk=smart_text(self.id),
            active=True
        ).order_by('-id')
        comments_json = CommentHandler(comments, user_id=user.id if user else None).render_comments_json()

        data.update({'cj': comments_json})

        return json.dumps(data)

    @staticmethod
    def get_queryset_by_param(p):
        if p == 'week':
            week = datetime.date.today() - datetime.timedelta(days=7)
            return Post.objects.filter(active=True, created_on__gt=week).order_by('-like_count')[:20]
        elif p == 'month':
            month = datetime.date.today() - datetime.timedelta(days=30)
            return Post.objects.filter(active=True, created_on__gt=month).order_by('-like_count')[:20]
        elif p == 'all':
            return Post.objects.filter(active=True).order_by('-like_count')[:20]


try:
    PostContentType = ContentType.objects.get_for_model(Post)
except:
    pass
