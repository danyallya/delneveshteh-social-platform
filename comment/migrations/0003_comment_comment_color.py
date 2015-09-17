# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20150831_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_color',
            field=models.CharField(default='#E6E6E6', verbose_name='رنگ', max_length=10),
        ),
    ]
