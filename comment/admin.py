from django.contrib import admin
from comment.models import Comment, ReportComment, LikeComment

admin.site.register(Comment)
admin.site.register(ReportComment)
admin.site.register(LikeComment)
