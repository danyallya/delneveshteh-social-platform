# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.datetime_safe
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='fav',
            field=models.BooleanField(verbose_name='علاقه مندی', default=False),
        ),
        migrations.AddField(
            model_name='reportcomment',
            name='created_on',
            field=models.DateTimeField(verbose_name='تاریخ ایجاد', default=django.utils.datetime_safe.datetime.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, default=None, related_name='children', on_delete=django.db.models.deletion.SET_NULL, to='comment.Comment', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='متن', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='کاربر', null=True),
        ),
        migrations.AlterField(
            model_name='reportcomment',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='کاربر'),
        ),
    ]
