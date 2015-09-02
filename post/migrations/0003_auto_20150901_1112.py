# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_auto_20150831_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostReport',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name_plural': 'گزارش پست',
                'verbose_name': 'گزارش پست',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(verbose_name='پسندیدن', default=0),
        ),
        migrations.AddField(
            model_name='postreport',
            name='post',
            field=models.ForeignKey(to='post.Post', verbose_name='پست'),
        ),
        migrations.AddField(
            model_name='postreport',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name='کاربر'),
        ),
    ]
