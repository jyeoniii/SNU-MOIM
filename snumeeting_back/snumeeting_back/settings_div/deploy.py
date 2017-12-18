from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# WSGI application
WSGI_APPLICATION = 'snumeeting_back.wsgi.deploy.application'

# Deploy mode -> DEBUG = False
DEBUG = False
