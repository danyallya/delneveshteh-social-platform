# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20151005_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='android_version',
            field=models.CharField(verbose_name='ورژن اندروید', default='', max_length=10),
        ),
        migrations.AddField(
            model_name='post',
            name='is_spec',
            field=models.BooleanField(verbose_name='داغ', default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.IntegerField(verbose_name='نوع', default=1),
        ),
        migrations.AddField(
            model_name='post',
            name='version_code',
            field=models.IntegerField(verbose_name='ورژن نرم افزار', default=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='comments_count',
            field=models.IntegerField(verbose_name='تعداد نظرها', null=True, default=0),
        ),
    ]
