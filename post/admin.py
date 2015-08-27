from django.contrib import admin
from post.models import Movie, Series, Telecast, MovieImage, Person, MovieRate
from utils.admin import HardModelAdmin


class ImagesInline(admin.TabularInline):
    model = MovieImage
    can_delete = True
    verbose_name_plural = u'تصاویر اثر'


class MovieAdmin(HardModelAdmin):
    inlines = (ImagesInline, )
    exclude = ['rate', 'rate_count']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, MovieAdmin)
admin.site.register(Telecast, MovieAdmin)
admin.site.register(Person)
admin.site.register(MovieRate)
