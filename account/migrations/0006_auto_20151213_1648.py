# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20151213_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='comments_count',
            field=models.IntegerField(null=True, default=0, verbose_name='تعداد نظرها'),
        ),
        migrations.AddField(
            model_name='profile',
            name='posts_count',
            field=models.IntegerField(default=0, verbose_name='تعداد پست ها'),
        ),
    ]
