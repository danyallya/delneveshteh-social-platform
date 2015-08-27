# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_basemovie_send_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemovie',
            name='send_notification',
            field=models.BooleanField(default=False, verbose_name='ارسال پیام برای ساخته شدن این اثر'),
        ),
    ]
