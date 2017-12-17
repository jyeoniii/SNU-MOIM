from .models import Ex_User, User, Subject
from django.forms.models import model_to_dict
from social_django.models import UserSocialAuth
from django.utils import timezone

import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def convert_userinfo_for_front(user_id):
  try:
    user_id = int(user_id)
    user = {}
    ex_user = Ex_User.objects.get(id=user_id)
    user['id'] = ex_user.id
    user['username'] = ex_user.user.username
    user['password'] = ex_user.user.password
    user['name'] = ex_user.name
    user['college'] = model_to_dict(ex_user.college)
    user['subjects'] = list(ex_user.subjects.all().values())
    user['fb_friends'] = fb_friends_userinfo_for_front(ex_user)
    try:
      ex_user.user.social_auth.get(provider='facebook')
      user['fb_connected'] = True
    except UserSocialAuth.DoesNotExist:
        user['fb_connected'] = False
    if ex_user.access_token == 'EXPIRED':
      user['token_expired'] = True
    else:
      user['token_expired'] = False
  except Ex_User.DoesNotExist:
    user['name'] = 'NONEXISTING'
  return user

def fb_friends_userinfo_for_front(ex_user):
  fb_friends = []
  for friend in ex_user.fb_friends.all():
    friend_info = {}
    friend_info['id'] = friend.id
    friend_info['name'] = friend.name
    friend_info['username'] = User.objects.get(id=friend.user_id).username
    fb_friends.append(friend_info)
  return fb_friends


def convert_userinfo_minimal(user_id):
  # convert user info - only minimal information needed (id+name)
  try:
    user_id = int(user_id)
    user = {}
    ex_user= Ex_User.objects.get(id=user_id)
    user['id'] = ex_user.id
    user['name'] = ex_user.name
  except Ex_User.DoesNotExist:
    user['name'] = 'NONEXISTING'
  return user

def convert_meeting_for_mainpage(meeting):
  user = {}
  d = model_to_dict(meeting)

  author_id = d['author']
  user = convert_userinfo_minimal(author_id)
  d['author'] = user

  subject_id = d['subject']
  d['subject'] = model_to_dict(Subject.objects.get(id=subject_id))
  d['members'] = list(meeting.members.all().values())
  d['datetime'] = convert_datetime(meeting.created_at)
  d.pop('tags')
  return d

def convert_datetime(datetime):
  res = {}
  datetime = timezone.localtime(datetime)
  res['year'] = datetime.year
  res['month'] = datetime.month
  res['day'] = datetime.day
  res['hour'] = datetime.hour
  if res['hour'] > 12:
    res['hour'] = res['hour'] - 12
    res['afternoon'] = True
  else:
    res['afternoon'] = False
  res['minute'] = datetime.minute
  res['second'] = datetime.second

  return res

def convert_fb_profile(ex_user):
    user_fb = {}
    social_user = ex_user.user.social_auth.get(provider='facebook')
    if social_user:
      url = u'https://graph.facebook.com/{0}?fields=name,picture' \
            u'&access_token={1}'.format(social_user.uid,social_user.extra_data['access_token'])
      http = urllib3.PoolManager()

      r = http.request('GET', url)
      response = json.loads(r.data)

      url = response['picture']['data']['url']
      name = response['name']

      user_fb['picture_url'] = url
      user_fb['fb_name'] = name
      user_fb['id'] = ex_user.id 
      user_fb['name'] = ex_user.name

    return user_fb 
    



