# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_remove_comment_comment_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='color',
            field=models.CharField(max_length=10, default='#E6E6E6', verbose_name='رنگ'),
        ),
    ]
