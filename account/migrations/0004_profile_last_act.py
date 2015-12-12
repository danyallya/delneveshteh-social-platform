# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150917_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_act',
            field=models.DateTimeField(verbose_name='آخرین حضور', blank=True, null=True),
        ),
    ]
