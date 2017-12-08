from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# WSGI application
WSGI_APPLICATION = 'snumeeting_back.wsgi.deploy.application'

# Static URLs
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# Deply mode -> DEBUG = False 
DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']
