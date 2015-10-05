from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from comment.models import Comment, ReportComment, LikeComment
from utils.admin import HardModelAdmin


class CommentAdmin(HardModelAdmin):
    list_display = ['user', 'get_post', 'like_count', 'get_desc', 'active']
    list_filter = ('created_on', 'like_count', 'active')
    search_fields = ('text',)

    fieldsets = (
        (None, {'fields': ('user', 'user_name', 'text', 'active', 'color')}),
    )

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = 'متن'

    def get_post(self, obj):
        link_obj = obj.content_type.model_class().objects.get(id=obj.object_pk)
        link = reverse('admin:%s_%s_change' % (link_obj._meta.app_label, link_obj._meta.model_name), args=[link_obj.id])
        return mark_safe("<a href='%s'>%s</a>" % (link, str(link_obj)))

    get_post.short_description = 'پست'


class LikeCommentAdmin(HardModelAdmin):
    list_display = ['user', 'get_comment']
    list_filter = ('created_on',)
    search_fields = ('comment__text',)
    list_display_links = ['user']

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = 'متن'

    def get_comment(self, obj):
        link_obj = obj.comment
        link = reverse('admin:%s_%s_change' % (link_obj._meta.app_label, link_obj._meta.model_name), args=[link_obj.id])
        return mark_safe("<a href='%s'>%s</a>" % (link, str(link_obj)))

    get_comment.short_description = 'کامنت'


class ReportCommentAdmin(HardModelAdmin):
    list_display = ['user', 'state', 'get_comment']
    list_filter = ('state', 'created_on')
    search_fields = ('comment__text',)

    def get_comment(self, obj):
        link_obj = obj.comment
        link = reverse('admin:%s_%s_change' % (link_obj._meta.app_label, link_obj._meta.model_name), args=[link_obj.id])
        return mark_safe("<a href='%s'>%s</a>" % (link, str(link_obj)))

    get_comment.short_description = 'کامنت'


admin.site.register(Comment, CommentAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
admin.site.register(LikeComment, LikeCommentAdmin)
