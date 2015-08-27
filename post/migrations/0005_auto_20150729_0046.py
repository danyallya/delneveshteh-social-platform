# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20150729_0001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movierate',
            options={'verbose_name': 'امتیاز کاربر', 'verbose_name_plural': 'امتیاز کاربران'},
        ),
    ]
