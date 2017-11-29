from django.shortcuts import redirect
from django.contrib import messages
from social_django.models import UserSocialAuth

from .models import Ex_User

import json

def check_user(strategy, user, request, **kwargs):
  if user is None and kwargs.get('is_new'):
    messages.error(request, 'To use this, you need to connect your account first.')
    return redirect('http://localhost:4200/sign_in')

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
