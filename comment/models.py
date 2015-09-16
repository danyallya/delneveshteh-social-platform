import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import Profile
from utils.templatetags.date_template_tags import pdate_if_date


class Comment(models.Model):
    user = models.ForeignKey(Profile, verbose_name="کاربر", null=True)
    user_name = models.CharField("نام", max_length=50, null=True, blank=True)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name='content type',
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField('object ID')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    text = models.TextField(null=True, verbose_name="متن")
    reply_to = models.ForeignKey('Comment', null=True, blank=True, default=None, related_name='children',
                                 on_delete=models.SET_NULL)
    like_count = models.IntegerField(verbose_name="پسندیدن", default=0)
    active = models.BooleanField(verbose_name="نمایش نظر", default=True)

    fav = models.BooleanField("علاقه مندی", default=False)

    def __str__(self):
        if len(self.text) > 31:
            return self.text[:30] + " ..."
        else:
            return self.text

    @property
    def color(self):
        if not self.active:
            return u"<font color='#aa0707'>تاییدنشده</font>"
        return u"<font color='#17c50a'>تاییدشده</font>"

    @property
    def reply(self):
        if not self.reply_to_id:
            return '---'
        return str(self.reply_to)

    def is_fav(self, user_id):
        if not user_id:
            return False
        return LikeComment.objects.filter(user_id=user_id, comment_id=self.id).exists()

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

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

    def update(self):
        self.like_count = self.likecomment_set.count()
        self.save()


class LikeComment(models.Model):
    user = models.ForeignKey(Profile, verbose_name="کاربر")
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    comment = models.ForeignKey(Comment, verbose_name="نظر")

    class Meta:
        verbose_name = "پسندیدن نظر"
        verbose_name_plural = "پسندیدن نظر"

    def __str__(self):
        return str(self.comment)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(LikeComment, self).save(force_insert, force_update, using, update_fields)
        self.comment.update()

    def delete(self, using=None):
        comment = self.comment
        super(LikeComment, self).delete(using)
        comment.update()


class ReportComment(models.Model):
    REPORT_STATES = (
        (1, "نامرتبط"),
        (2, "موهن"),
        (3, "نامناسب")
    )
    user = models.ForeignKey(Profile, verbose_name="کاربر", null=True, blank=True)
    comment = models.ForeignKey(Comment, verbose_name="نظر")
    state = models.IntegerField(verbose_name="نوع", default=1, choices=REPORT_STATES)
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "گزارش نظر"
        verbose_name_plural = "گزارش نظرات"

    def __str__(self):
        return str(self.comment)
