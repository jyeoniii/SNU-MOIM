from .models import Ex_User, User, Subject
from django.forms.models import model_to_dict
from social_django.models import UserSocialAuth
from django.utils import timezone

def convert_userinfo_for_front(user_id):
  try:
    user_id = int(user_id)
    user = {}
    ex_user = Ex_User.objects.get(id=user_id)
    user['id'] = ex_user.id
    user['username'] = ex_user.user.username
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
