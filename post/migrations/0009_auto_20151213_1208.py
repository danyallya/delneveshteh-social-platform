# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20151211_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='android_version',
            field=models.IntegerField(verbose_name='ورژن اندروید', default=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.IntegerField(verbose_name='نوع', choices=[(1, 'دلنوشته'), (2, 'بحث'), (3, 'مناسبت'), (4, 'حدیث')], default=1),
        ),
    ]
