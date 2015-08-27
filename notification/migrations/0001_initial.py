# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='نام', max_length=500)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('text', models.TextField(null=True, verbose_name='متن')),
                ('receive_count', models.IntegerField(null=True)),
                ('creator', models.ForeignKey(blank=True, verbose_name='سازنده', to=settings.AUTH_USER_MODEL, null=True)),
                ('post', models.ForeignKey(blank=True, to='post.Post', null=True)),
            ],
            options={
                'verbose_name_plural': 'پیام ها',
                'verbose_name': 'پیام',
            },
        ),
    ]
