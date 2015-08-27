from django.db import models


class Named(models.Model):
    name = models.CharField(verbose_name="نام", max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseModel(Named):
    creator = models.ForeignKey('account.Profile', verbose_name="سازنده", null=True, blank=True)
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
