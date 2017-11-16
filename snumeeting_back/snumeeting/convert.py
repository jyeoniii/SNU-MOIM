from .models import Ex_User, User, Subject
from django.forms.models import model_to_dict

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
  except Ex_User.DoesNotExist:
    user['name'] = 'NONEXISTING'
  return user

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
  d['members']=list(meeting.members.all().values())
  return d


