from django.conf import settings

__author__ = 'M.Y'


def default_settings(request):
    return {"LANGUAGE_CODE": settings.LANGUAGE_CODE, "LANGUAGE_BIDI": True}