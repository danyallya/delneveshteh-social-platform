# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20150729_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='basemovie',
            name='rate_count',
            field=models.IntegerField(default=0, verbose_name='تعداد امتیازها'),
        ),
    ]
