# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMovie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=500, verbose_name='نام')),
                ('created_on', models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to='movie_images', verbose_name='تصویر')),
                ('year_produce', models.IntegerField(null=True, verbose_name='سال تولید')),
                ('genre', models.IntegerField(choices=[(1, 'جنایی'), (2, 'اکشن')], null=True, verbose_name='گونه')),
                ('margins', models.TextField(null=True, verbose_name='حاشیه')),
                ('trailer', models.FileField(null=True, upload_to='movie_trailers', verbose_name='تیزر')),
                ('active', models.BooleanField(verbose_name='نمایش اثر', default=True)),
                ('rate', models.FloatField(verbose_name='امتیاز', default=0)),
            ],
            options={
                'verbose_name_plural': 'فیلم ها',
                'verbose_name': 'فیلم',
                'get_latest_by': 'created_on',
            },
        ),
        migrations.CreateModel(
            name='MovieImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(upload_to='movie_extra_images', verbose_name='تصویر')),
            ],
            options={
                'verbose_name_plural': 'تصاویر اثر',
                'verbose_name': 'تصویر اثر',
            },
        ),
        migrations.CreateModel(
            name='MovieRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('rate', models.IntegerField(verbose_name='امتیاز')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name_plural': 'امتیازها',
                'verbose_name': 'امتیاز',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=500, verbose_name='نام')),
            ],
            options={
                'verbose_name_plural': 'اشخاص',
                'verbose_name': 'شخص',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('basemovie_ptr', models.OneToOneField(to='post.BaseMovie', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('length', models.CharField(max_length=255, null=True, verbose_name='مدت زمان')),
                ('brief', models.TextField(null=True, verbose_name='خلاصه داستان')),
                ('actors', models.ManyToManyField(related_name='movie_actors', to='post.Person', verbose_name='بازیگران اصلی')),
                ('author', models.ForeignKey(related_name='movie_authors', to='post.Person', null=True, verbose_name='نویسنده')),
                ('camera_director', models.ForeignKey(related_name='movie_camera_directors', to='post.Person', null=True, verbose_name='مدیر فیلم برداری')),
                ('composer', models.ForeignKey(related_name='movie_composers', to='post.Person', null=True, verbose_name='آهنگ ساز')),
            ],
            options={
                'verbose_name_plural': 'فیلم های سینمایی',
                'verbose_name': 'فیلم سینمایی',
                'get_latest_by': 'created_on',
            },
            bases=('movie.basemovie',),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('basemovie_ptr', models.OneToOneField(to='post.BaseMovie', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('show_time', models.CharField(max_length=255, null=True, verbose_name='زمان پخش')),
                ('titrag', models.FileField(null=True, upload_to='movie_credits', verbose_name='تیتراژ')),
                ('brief', models.TextField(null=True, verbose_name='خلاصه داستان')),
                ('actors', models.ManyToManyField(related_name='series_actors', to='post.Person', verbose_name='بازیگران اصلی')),
                ('author', models.ForeignKey(related_name='series_authors', to='post.Person', null=True, verbose_name='نویسنده')),
                ('camera_director', models.ForeignKey(related_name='series_camera_director', to='post.Person', null=True, verbose_name='مدیر فیلم برداری')),
                ('composer', models.ForeignKey(related_name='series_composers', to='post.Person', null=True, verbose_name='آهنگ ساز')),
            ],
            options={
                'verbose_name_plural': 'سریال ها',
                'verbose_name': 'سریال',
                'get_latest_by': 'created_on',
            },
            bases=('movie.basemovie',),
        ),
        migrations.CreateModel(
            name='Telecast',
            fields=[
                ('basemovie_ptr', models.OneToOneField(to='post.BaseMovie', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('length', models.CharField(max_length=255, null=True, verbose_name='مدت زمان')),
                ('show_time', models.CharField(max_length=255, null=True, verbose_name='زمان پخش')),
                ('about', models.TextField(null=True, verbose_name='درباره برنامه')),
                ('channel', models.CharField(max_length=255, null=True, verbose_name='شبکه تلویزیونی')),
                ('presenter', models.ForeignKey(related_name='presenters', to='post.Person', null=True, verbose_name='مجری')),
            ],
            options={
                'verbose_name_plural': 'برنامه های تلویزیونی',
                'verbose_name': 'برنامه تلویزیونی',
                'get_latest_by': 'created_on',
            },
            bases=('movie.basemovie',),
        ),
        migrations.AddField(
            model_name='movieimage',
            name='movie',
            field=models.ForeignKey(related_name='extra_images', to='post.BaseMovie', null=True, verbose_name='اثر'),
        ),
        migrations.AddField(
            model_name='basemovie',
            name='creator',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='سازنده'),
        ),
        migrations.AddField(
            model_name='basemovie',
            name='director',
            field=models.ForeignKey(related_name='directors', to='post.Person', null=True, verbose_name='کارگردان'),
        ),
        migrations.AddField(
            model_name='basemovie',
            name='others',
            field=models.ManyToManyField(to='post.Person', verbose_name='سایر عوامل'),
        ),
        migrations.AddField(
            model_name='basemovie',
            name='producer',
            field=models.ForeignKey(related_name='producers', to='post.Person', null=True, verbose_name='تهیه کننده'),
        ),
    ]
