# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemovie',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to='movie_trailers', verbose_name='تیزر'),
        ),
        migrations.AlterField(
            model_name='series',
            name='titrag',
            field=models.FileField(blank=True, null=True, upload_to='movie_credits', verbose_name='تیتراژ'),
        ),
    ]
