from builtins import staticmethod
import datetime
import json
from django.db import models
from django.db.models.query_utils import Q
from django.db.transaction import atomic

from utils.models import BaseModel


class Notification(BaseModel):
    text = models.TextField(verbose_name="متن", null=True)
    receive_count = models.IntegerField(null=True, default=0, verbose_name="تعداد دریافت")
    post = models.ForeignKey('post.Post', null=True, blank=True)
    expire_date = models.DateField(verbose_name="تاریخ انقضا", default=None, null=True)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        if len(self.text) > 31:
            return self.text[:30] + " ..."
        else:
            return self.text

    @staticmethod
    @atomic
    def get_notification_json(last_id, user):
        today = datetime.date.today()
        notifs = Notification.objects.filter(id__gt=last_id). \
            filter(Q(expire_date__gte=today) | Q(expire_date__isnull=True))
        res = []
        for notif in notifs:
            notif_dict = {'i': notif.id, 'n': notif.name, 't': notif.text, 'm': notif.movie_id or 0}
            if notif.movie_id:
                summery = notif.movie.get_summery_fields(user)
                notif_dict.update({'ms': summery})
            res.append(notif_dict)
            notif.receive_count += 1
            notif.save()

        return json.dumps(res)


Notification._meta.get_field('name').verbose_name = 'عنوان'
