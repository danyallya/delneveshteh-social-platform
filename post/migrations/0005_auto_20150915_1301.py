# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20150902_0911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='rate_count',
            new_name='comments_count',
        ),
    ]
