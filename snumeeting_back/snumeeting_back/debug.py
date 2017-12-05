from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

# WSGI application 
WSGI_APPLICATION = 'snumeeting_back.wsgi.debug.application'

# Debug mode -> DEBUG = True
DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']
