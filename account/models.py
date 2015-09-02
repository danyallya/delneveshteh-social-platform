from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import BaseModel


class Profile(AbstractUser):
    # birth_date = models.DateField(verbose_name="تاریخ تولد", null=True)
    # image = models.ImageField(blank=True, null=True, upload_to='user_images/')

    def __str__(self):
        return self.name

    # @property
    # def standard_birth(self):
    #     if self.birth_date:
    #         return self.birth_date.strftime("%Y-%m-%d")

    # @property
    # def age(self):
    #     if self.birth_date:
    #         return date.today().year - self.birth_date.year

    @property
    def name(self):
        return self.username

    def get_android_fields(self):
        return {'u': self.username, 'e': self.email}
        # @property
        # def profile_image(self):
        #     if self.image:
        #         # print('%s%s' % (settings.MEDIA_URL, self.image))
        #         return '%s%s' % (settings.MEDIA_URL, self.image)
        #     else:
        #         return '/static/img/temp.jpg'


class Suggestion(BaseModel):
    SUGGESTION_TYPES = (
        (1, "پیشنهاد"),
        (2, "انتقاد"),
        (3, "نظر"),
        (4, "سفارش تبلیغات"),
    )
    sug_type = models.IntegerField(verbose_name="نوع", null=True, default=1, choices=SUGGESTION_TYPES)
    email = models.EmailField(verbose_name=u"ایمیل", null=True)
    title = models.CharField(verbose_name=u"عنوان", null=True, max_length=700)
    body = models.CharField(verbose_name=u"متن", null=True, max_length=3000)

    class Meta:
        verbose_name = u"تماس با ما"
        verbose_name_plural = u"تماس با ما"

    def __str__(self):
        return self.title
