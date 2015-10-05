# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='expire_date',
            field=models.DateField(verbose_name='تاریخ انقضا', null=True, default=None),
        ),
        migrations.AlterField(
            model_name='notification',
            name='receive_count',
            field=models.IntegerField(verbose_name='تعداد دریافت', null=True, default=0),
        ),
    ]
