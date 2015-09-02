from django.contrib import admin

from post.models import Post, PostReport, PostLike
from utils.admin import HardModelAdmin


class ReportPostAdmin(HardModelAdmin):
    list_display = ['user', 'get_desc']
    list_filter = ('created_on',)
    search_fields = ('post__text',)

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = 'پست'


admin.site.register(PostReport, ReportPostAdmin)


class PostLikeAdmin(HardModelAdmin):
    list_display = ['user', 'get_desc']
    list_filter = ('created_on',)
    search_fields = ('post__text',)

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = 'پست'


admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(Post)
