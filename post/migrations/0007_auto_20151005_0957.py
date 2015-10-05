# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='color',
            field=colorful.fields.RGBColorField(default='#528c8a', verbose_name='رنگ'),
        ),
    ]
