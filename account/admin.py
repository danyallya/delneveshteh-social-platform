from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Suggestion, Profile
from utils.admin import HardModelAdmin

admin.site.register(Suggestion, HardModelAdmin)


class UserProfileAdmin(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('username', 'email', 'post_count', 'comment_count', 'like_count', 'report_count', 'is_staff')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = u"پست"

    def comment_count(self, obj):
        return obj.comment_set.count()

    comment_count.short_description = u"کامنت"

    def like_count(self, obj):
        return obj.postlike_set.count()

    like_count.short_description = u"پسندیدن"

    def report_count(self, obj):
        return obj.postreport_set.count()

    report_count.short_description = u"تعداد گزارش کردن"

    # inlines = (ProfileInline, )
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
    #                                    'groups', 'user_permissions')}),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # list_display = ('username', 'email', 'first_name', 'last_name', 'get_gender', 'description', 'get_created_date')
    #
    # list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__gender', 'profile__created_on')
    # search_fields = ('username', 'first_name', 'last_name', 'email')

    # def description(self, obj):
    #     return mark_safe(
    #         obj.profile.description.replace('\r\n', '<br/>').replace('\n\r', '<br/>').replace('\r', '<br/>').replace(
    #             '\n', '<br/>'))
    #
    # description.allow_tags = True
    # description.short_description = 'توضیحات'

    # def get_created_date(self, obj):
    #     return jalali(obj.profile.created_on)

    # get_created_date.short_description = u"تاریخ ایجاد"
    # get_created_date.admin_order_field = 'profile__created_on'
    #
    # def get_gender(self, obj):
    #     return obj.profile.get_gender_display()
    #
    # get_gender.short_description = u"جنسیت"
    # get_gender.admin_order_field = 'profile__gender'
    #
    # def save_model(self, request, obj, form, change):
    #     obj.save()
    #     try:
    #         obj.profile
    #     except Profile.DoesNotExist:
    #         Profile.objects.create(user=obj, active=True)


admin.site.register(Profile, UserProfileAdmin)
