# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20151213_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='month_posts_count',
            field=models.IntegerField(verbose_name='تعداد پست های ماه', default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='week_posts_count',
            field=models.IntegerField(verbose_name='تعداد پست های هفته', default=0),
        ),
    ]
