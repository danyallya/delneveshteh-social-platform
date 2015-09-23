"""
WSGI config for prk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/apps/delnev')
sys.path.append('/home/apps/delnev/nevesht')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nevesht.settings")

# serve django via WSGI
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
