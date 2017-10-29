
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict
from .models import Ex_User, Meeting, Comment, Subject, College
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
import json

# url: /signup
def signup(request):
  if request.method == 'POST':
    req_data = json.loads(request.body.decode())
    username = req_data['name']
    password = req_data['password']
    email = req_data['mySNU']
    user = User.objects.create_user(username=username, password=password, email=email)
    user.ex_User.college = req_data['college']
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['POST'])


@ensure_csrf_cookie
def token(request):
  if request.method == 'GET':
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'])

# url: /signin
def signin(request):
  if request.method == 'POST':
    req_data = json.loads(request.body.decode())
    email = req_data['mySNU']
    password = req_data['password']
    user = authenticate(email=emial,password=password)
    if user is not None:
      login(request, user)
      return HttpResponse(status=200)
    else:
      return HttpResponse(status=401)
  else:
    return HttpResponseNotAllowed(['POST'])

# url: /signout
def signout(request):
  if request.method == 'GET':
    logout(request)
    response = redirect('signin')
    response.delete_cookie('user_location')
    return response
  else:
    return HttpResponseNotAllowed(['GET'])
"""
# url: /user/:id
def userDetail(request, user_id):
  user_id = int(user_id)
  if request.method == 'GET':
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(model_to_dict(user))
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode()) # Deserialized request
    username = des_req['name']
    password = des_req['password']
    email = des_req['mySNU']
    college = des_req['college']
    try:
      user = User.objects.get(id=user_id)
      user.username = username
      user.password = password
      user.email = email
      user.ex_User.college = college
      user.ex_User.save()
      user.save()
    except User.DoesNotExist:
      return HttpResponseNotFound()
    return HttpResponse(status=204)
  elif request.method == 'DELETE':
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return HttpResponseNotFound()
    user.delete()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['PUT'],['DELETE'])

# url: /meeting
def meetingList(request):
  if request.method == 'GET':
    return JsonResponse(list(Meeting.objects.all().values()), safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author = des_req['author']
    title = des_req['title']
    description = des_req['description']
    location = des_req['location']
    max_member = des_req['max_member']
    members = des_req['members']
    subject = des_req['subject']
    new_meeting = Meeting(author=author, title=title, description=description, location=location, max_member=max_member, members=members, subject=subject)
    new_meeting.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /meeting/:id
def meetingDetail(request, meeting_id):
  meeting_id = int(meeting_id)
  if request.method == 'GET':
    try:
      meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(model_to_dict(meeting))
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['PUT'],['DELETE'])

# url: /meeting/:id/comment
def meetingComment(request, meeting_id):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])

# url: /comment
def commentList(request):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])

# url: /comment/:id
def commentDetail(request, comment_id):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])

# url: /subject
def subjectList(request):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])

# url: /subject/:id
def subjectDetail(request, subject_id):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])

# url: /college
def collegeList(request):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])

# url: /college/:id
def collegeList(request, college_id):
  if request.method == 'GET':

  elif request.method == 'POST':
    
  elif request.method == 'PUT':

  elif request.method == 'DELETE':

  else:
    return HttpResponseNotAllowed(['GET'],['POST'],['PUT'],['DELETE'])
"""
