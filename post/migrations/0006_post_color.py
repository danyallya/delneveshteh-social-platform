# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20150915_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='color',
            field=models.CharField(verbose_name='رنگ', max_length=10, default='#528c8a'),
        ),
    ]
