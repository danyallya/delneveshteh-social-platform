from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from post.models import Post, PostReport, PostLike
from utils.admin import HardModelAdmin


class ReportPostAdmin(HardModelAdmin):
    list_display = ['user', 'get_post', ]
    list_filter = ('created_on',)
    search_fields = ('post__text',)

    def get_post(self, obj):
        link_obj = obj.post
        link = reverse('admin:%s_%s_change' % (link_obj._meta.app_label, link_obj._meta.model_name), args=[link_obj.id])
        return mark_safe("<a href='%s'>%s</a>" % (link, str(link_obj)))

    get_post.short_description = 'پست'


admin.site.register(PostReport, ReportPostAdmin)


class PostLikeAdmin(HardModelAdmin):
    list_display = ['user', 'get_post']
    list_filter = ('created_on',)
    search_fields = ('post__text',)

    def get_post(self, obj):
        link_obj = obj.post
        link = reverse('admin:%s_%s_change' % (link_obj._meta.app_label, link_obj._meta.model_name), args=[link_obj.id])
        return mark_safe("<a href='%s'>%s</a>" % (link, str(link_obj)))

    get_post.short_description = 'پست'


class PostAdmin(HardModelAdmin):
    list_display = ['creator', 'get_text', 'like_count', 'comments_count', 'active']
    list_filter = ('created_on',)
    search_fields = ('text', 'creator__username')

    def get_text(self, obj):
        return str(obj)

    get_text.short_description = 'متن'


admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(Post, PostAdmin)
