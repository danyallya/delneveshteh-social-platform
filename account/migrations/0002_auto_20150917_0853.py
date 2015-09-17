# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestion',
            name='title',
        ),
        migrations.AddField(
            model_name='suggestion',
            name='phone',
            field=models.CharField(max_length=100, verbose_name='شماره تماس', null=True),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='body',
            field=models.TextField(max_length=3000, verbose_name='متن', null=True),
        ),
    ]
