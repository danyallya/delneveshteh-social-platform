# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20150901_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlike',
            name='created_time',
        ),
        migrations.AddField(
            model_name='postlike',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postrate',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
    ]
