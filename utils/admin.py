# -*- coding:utf-8 -*-
from django.contrib import admin
from easy_select2.utils import select2_modelform
# from mce_filebrowser.admin import MCEFilebrowserAdmin

from utils.calverter import gregorian_to_jalali


__author__ = 'M.Y'


class HardModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.num = 0
        self.form = select2_modelform(model, attrs={'width': '250px'})
        super(HardModelAdmin, self).__init__(model, admin_site)
        # self.list_display = ['get_row_num'] + list(self.list_display)
        if 'created_on' in model._meta.get_all_field_names():
            self.list_display = list(self.list_display) + ['get_created_date']
        if 'creator' in model._meta.get_all_field_names():
            self.exclude = [] if not self.exclude else self.exclude
            if 'creator' not in self.exclude:
                self.exclude += ['creator', ]
        if not self.list_display_links:
            self.list_display_links = self.list_display[:2]
            # self.list_editable = ['name']

    def get_created_date(self, obj):
        return gregorian_to_jalali(obj.created_on)

    get_created_date.short_description = u"تاریخ ایجاد"
    get_created_date.admin_order_field = 'created_on'

    def get_row_num(self, obj):
        self.num += 1
        return self.num

    get_row_num.short_description = u"ردیف"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        obj.save()
