import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snumeeting_back.settings_div.debug")
application = get_wsgi_application()