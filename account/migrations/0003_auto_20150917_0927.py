# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150917_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='sug_type',
            field=models.IntegerField(verbose_name='نوع', null=True, choices=[(1, 'پیشنهاد و انتقاد'), (2, 'تبلیغات'), (3, 'ثبت سفارش')], default=1),
        ),
    ]
