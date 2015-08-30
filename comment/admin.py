from django.contrib import admin

from comment.models import Comment, ReportComment, LikeComment
from utils.admin import HardModelAdmin


class CommentAdmin(HardModelAdmin):
    list_display = ['user', 'like_count', 'get_desc', 'active', 'get_reply']
    list_filter = ('created_on', 'like_count', 'active', 'fav')
    search_fields = ('text',)

    fieldsets = (
        (None, {'fields': ('user', 'user_name', 'text', 'active')}),
    )

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = u"„ ‰"

    def get_reply(self, obj):
        return str(obj.reply)

    get_reply.short_description = u"‰Ÿ— «’·?"


class LikeCommentAdmin(HardModelAdmin):
    list_display = ['user', 'comment']
    list_filter = ('created_on',)
    search_fields = ('comment__text',)
    list_display_links = ['user']

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = u"„ ‰"

    def get_reply(self, obj):
        return str(obj.reply)

    get_reply.short_description = u"‰Ÿ— «’·?"


class ReportCommentAdmin(HardModelAdmin):
    list_display = ['user', 'state', 'get_desc']
    list_filter = ('state', 'created_on')
    search_fields = ('comment_text',)

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = u"ò«„‰ "


admin.site.register(Comment, CommentAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
admin.site.register(LikeComment, LikeCommentAdmin)
