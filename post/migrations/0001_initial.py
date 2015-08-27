# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='نام', max_length=500)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('text', models.TextField()),
                ('active', models.BooleanField(default=True, verbose_name='نمایش')),
                ('rate', models.FloatField(default=0, null=True, verbose_name='امتیاز')),
                ('rate_count', models.IntegerField(default=0, null=True, verbose_name='تعداد امتیازها')),
                ('creator', models.ForeignKey(blank=True, verbose_name='سازنده', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'فیلم ها',
                'get_latest_by': 'created_on',
                'verbose_name': 'فیلم',
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to='extra_images', verbose_name='تصویر')),
                ('movie', models.ForeignKey(related_name='extra_images', verbose_name='اثر', to='post.Post', null=True)),
            ],
            options={
                'verbose_name_plural': 'تصاویر اثر',
                'verbose_name': 'تصویر اثر',
            },
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(related_name='likes', verbose_name='پست', to='post.Post')),
                ('user', models.ForeignKey(verbose_name='کاربر', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'پسندیدن  ها',
                'verbose_name': 'پسندیدن',
            },
        ),
        migrations.CreateModel(
            name='PostRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rate', models.IntegerField(verbose_name='امتیاز')),
                ('user', models.ForeignKey(verbose_name='کاربر', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'امتیاز کاربران',
                'verbose_name': 'امتیاز کاربر',
            },
        ),
    ]
