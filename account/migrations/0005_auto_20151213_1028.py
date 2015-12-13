# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_last_act'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_act',
            field=models.DateTimeField(null=True, verbose_name='آخرین حضور', auto_now=True),
        ),
    ]
