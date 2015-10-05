from django.contrib import admin

from notification.models import Notification
from utils.admin import HardModelAdmin


class NotificationAdmin(HardModelAdmin):
    list_display = ['name', 'post', 'get_desc', 'receive_count', 'expire_date']
    list_filter = ('created_on', 'expire_date',)
    search_fields = ('text', 'name')

    def get_desc(self, obj):
        return str(obj)

    get_desc.short_description = u"متن"


admin.site.register(Notification, NotificationAdmin)
