# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20150728_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='basemovie',
            name='send_notification',
            field=models.BooleanField(default=False),
        ),
    ]
