from django.db import models
from post.models import Post

from utils.models import BaseModel


class Notification(BaseModel):
    text = models.TextField(verbose_name="متن", null=True)
    receive_count = models.IntegerField(null=True)
    post = models.ForeignKey(Post, null=True, blank=True)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"


Notification._meta.get_field('name').verbose_name = 'عنوان'
