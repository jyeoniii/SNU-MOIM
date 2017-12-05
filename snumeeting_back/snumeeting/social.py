from django.shortcuts import redirect
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.core.exceptions import ImproperlyConfigured

from .models import Ex_User

import os
import json
import requests

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_env(setting, envs):
  try:
    return envs[setting]
  except:
    error_msg = 'You should set {} environ'.format(setting)
    raise ImproperlyConfigured(error_msg)

def check_user(strategy, user, request, **kwargs):
  print(kwargs)

  if user is None and kwargs['is_new']:
    messages.error(request, 'To use this, you need to connect your account first.')
    return redirect('http://localhost:4200/sign_in')

  try:
    uid = user.social_auth.get(provider='facebook').uid
    if kwargs['response']['id'] != uid:
      messages.error(request, 'This snu-moim ID is already connected to another Facebook account.')
      return redirect('http://localhost:4200/sign_in')
  except Exception:
    pass

  try:
    fb_user = UserSocialAuth.get_social_auth('facebook', kwargs['response']['id']).user
    if user.id != fb_user.id:
      messages.error(request, 'This Facebook account is already connected to another snu-moim ID.')
      return redirect('http://localhost:4200/sign_in')
  except Exception:
    pass



def save_access_token(strategy, user, request, **kwargs):
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

  token = kwargs['response']['access_token']

  url = ('https://graph.facebook.com/v2.11/oauth/access_token?grant_type=fb_exchange_token' +
         '&client_id=' +  FACEBOOK_KEY +
         '&client_secret=' + FACEBOOK_SECRET +
         '&fb_exchange_token=' + token)

  response = requests.get(url)
  token = response.json()['access_token']

  ex_user = Ex_User.objects.get(user = user)
  ex_user.access_token = token
  ex_user.save()

def save_friends_data(strategy, user, request, **kwargs):
  ex_user = Ex_User.objects.get(user = user)
  friends = kwargs['response']['friends']['data']

  for friend in friends:
    try:
      friend_by_id = UserSocialAuth.get_social_auth('facebook', friend['id']).user
      if friend_by_id is not None:
        try:
          ex_user_friend = Ex_User.objects.get(user = friend_by_id)
          ex_user.fb_friends.add(ex_user_friend)
        except Exception:
          pass
    except Exception:
      pass

  ex_user.save()
