"""
Django settings for snumeeting_back project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json

from django.core.exceptions import ImproperlyConfigured

import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CONFIG_SECRET_DIR = os.path.join(BASE_DIR, '.config_secret')
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')

config_secret_common = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())
SECRET_KEY = config_secret_common['django']['secret_key']

CONFIG_SECRET_DEBUG_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_debug.json')
CONFIG_SECRET_DEPLOY_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_deploy.json')



def get_env(setting, envs):
  try:
    return envs[setting]
  except:
    error_msg = 'You should set {} environ'.format(setting)
    raise ImproperlyConfigured(error_msg)

DEV_ENVS = os.path.join(BASE_DIR, "envs_dev.json")
DEPLOY_ENVS = os.path.join(BASE_DIR, "envs.json")

if os.path.exists(DEV_ENVS):  # Develop Env
  env_file = open(DEV_ENVS)
elif os.path.exists(DEPLOY_ENVS):
  env_file = open(DEPLOY_ENVS)  # Deploy Env
else:
  env_file = None

if env_file is None: # System environ
  try:
    FACEBOOK_KEY = os.environ['FACEBOOK_KEY']
    FACEBOOK_SECRET = os.environ['FACEBOOK_SECRET']
  except KeyError as error_msg:
    raise ImproperlyConfigured(error_msg)
else:
  envs = json.loads(env_file.read())
  FACEBOOK_KEY = get_env('FACEBOOK_KEY', envs)
  FACEBOOK_SECRET = get_env('FACEBOOK_SECRET', envs)

# SocialLogin: Facebook
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['user_friends']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
   'fields': 'id, name, friends'
}
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL='http://localhost:4200/meeting'

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
LOGIN_ERROR_URL='http://localhost:4200/signin'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'x(ail4w!6kt8n+g%aqofbvs3x2lx8crd6sneer-%e!t!npf!7q'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '52.78.119.61',
    'snu-moim.ga',
    'ec2-52-78-119-61.ap-northeast-2.compute.amazonaws.com'
]

ANGULAR_APP_DIR = os.path.join(BASE_DIR, 'front/dist')

STATICFILES_DIRS = [
    os.path.join(ANGULAR_APP_DIR),
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Application definition

INSTALLED_APPS = [
    'snumeeting.apps.SnumeetingConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',                    # For social login service
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',    
]

MIDDLEWARE = [
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'        
]

ROOT_URLCONF = 'snumeeting_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'snumeeting_back.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'snumoimDB',
        'USER': 'snumoim_user', # database account 
        'PASSWORD': 'tmsnahdla', # account password 
        'HOST': '52.78.119.61', # database address (IP)
        'PORT': '3306', # database port(normally 3306)
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Sending e-mail (for verification)
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'snu.moim@gmail.com'
EMAIL_HOST_PASSWORD = '2017snumoim'
EMAIL_PORT = 587


# Facebook Login
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'snumeeting.social.check_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'snumeeting.social.save_access_token',
    'snumeeting.social.save_friends_data',
)


LOGIN_REDIRECT_URL = 'http://localhost:4200/meeting'
