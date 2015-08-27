# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_basemovie_rate_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemovie',
            name='rate',
            field=models.FloatField(verbose_name='امتیاز', default=0, null=True),
        ),
        migrations.AlterField(
            model_name='basemovie',
            name='rate_count',
            field=models.IntegerField(verbose_name='تعداد امتیازها', default=0, null=True),
        ),
    ]
