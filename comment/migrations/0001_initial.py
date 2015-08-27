# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, null=True, verbose_name='نام', max_length=50)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('text', models.TextField(null=True)),
                ('like_count', models.IntegerField(default=0, verbose_name='پسندیدن')),
                ('active', models.BooleanField(default=True, verbose_name='نمایش نظر')),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_comment', verbose_name='content type', to='contenttypes.ContentType')),
                ('reply_to', models.ForeignKey(blank=True, related_name='children', to='comment.Comment', default=None, null=True)),
                ('user', models.ForeignKey(verbose_name='کاربر', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'نظرات',
                'verbose_name': 'نظر',
            },
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('comment', models.ForeignKey(verbose_name='نظر', to='comment.Comment')),
                ('user', models.ForeignKey(verbose_name='کاربر', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'پسندیدن نظر',
                'verbose_name': 'پسندیدن نظر',
            },
        ),
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('state', models.IntegerField(default=1, choices=[(1, 'نامرتبط'), (2, 'موهن'), (3, 'نامناسب')], verbose_name='نوع')),
                ('comment', models.ForeignKey(verbose_name='نظر', to='comment.Comment')),
                ('user', models.ForeignKey(verbose_name='کاربر', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'گزارش نظرات',
                'verbose_name': 'گزارش نظر',
            },
        ),
    ]
