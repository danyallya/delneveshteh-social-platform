# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_comment_comment_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_color',
        ),
    ]
