from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import Profile


class Comment(models.Model):
    user = models.ForeignKey(Profile, verbose_name="کاربر")
    user_name = models.CharField("نام", max_length=50, null=True, blank=True)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name='content type',
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField('object ID')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    text = models.TextField(null=True)
    reply_to = models.ForeignKey('Comment', null=True, blank=True, default=None, related_name='children')
    like_count = models.IntegerField(verbose_name="پسندیدن", default=0)
    active = models.BooleanField(verbose_name="نمایش نظر", default=True)

    @property
    def color(self):
        if not self.active:
            return u"<font color='#aa0707'>تاییدنشده</font>"
        return u"<font color='#17c50a'>تاییدشده</font>"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"


class LikeComment(models.Model):
    user = models.ForeignKey(Profile, verbose_name="کاربر")
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    comment = models.ForeignKey(Comment, verbose_name="نظر")

    class Meta:
        verbose_name = "پسندیدن نظر"
        verbose_name_plural = "پسندیدن نظر"


class ReportComment(models.Model):
    REPORT_STATES = (
        (1, "نامرتبط"),
        (2, "موهن"),
        (3, "نامناسب")
    )
    user = models.ForeignKey(Profile, verbose_name="کاربر")
    comment = models.ForeignKey(Comment, verbose_name="نظر")
    state = models.IntegerField(verbose_name="نوع", default=1, choices=REPORT_STATES)

    class Meta:
        verbose_name = "گزارش نظر"
        verbose_name_plural = "گزارش نظرات"
