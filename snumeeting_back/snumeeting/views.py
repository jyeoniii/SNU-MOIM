from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict
from .models import Ex_User, Meeting, Comment, Subject, College
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
import json

# url: /signup
def signup(request):
  if request.method == 'POST':
    req_data = json.loads(request.body.decode())
    username = req_data['name']
    password = req_data['password']
    email = req_data['mySNU']
    college_id = req_data['college_id'] # instead of getting object, gets id first
    college = College.objects.get(id=college_id) # gets the object by id
    subject_ids = req_data['subject_ids']
    subjects = Subject.objects.filter(id__in=subject_ids) # gets the objects by ids
    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    ex_User = Ex_User.objects.create(user=user, college=college) # create first, m2m later
    ex_User.save()
    ex_User.subjects.add(*subjects) # adding many-to-many at once
    ex_User.save()
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
    user = User.objects.filter(email=email).first()
    if user is not None:
      username = user.username
    else:
      username = ''
    password = req_data['password']
    user = authenticate(request, username=username, password=password)
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
    return HttpResponse(status=200)
  else:
    return HttpResponseNotAllowed(['GET'])

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
    req_data = json.loads(request.body.decode())
    username = req_data['name']
    password = req_data['password']
    email = req_data['mySNU']
    college_id = req_data['college_id'] # instead of getting object, gets id first
    college = College.objects.get(id=college_id) # gets the object by id
    subject_ids = req_data['subject_ids']
    subjects = Subject.objects.filter(id__in=subject_ids) # gets the objects by ids
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return HttpResponseNotFound()
    user.username = username
    user.password = password
    user.email = email
    user.extendedUser.college = college
    user.extendedUser.subjects.clear()
    user.extendedUser.subjects.add(*subjects)
    user.extendedUser.save()
    user.save()
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
    meetings = Meeting.objects.all()
    dict_meetings = []
    for meeting in meetings:
      d = model_to_dict(meeting)
      d['members']=list(meeting.members.all().values())
      dict_meetings.append(d)
    return JsonResponse(dict_meetings, safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = User.objects.get(id=author_id)
    title = des_req['title']
    description = des_req['description']
    location = des_req['location']
    max_member = des_req['max_member']
    member_ids = des_req['member_ids']
    members = User.objects.filter(id__in=member_ids)
    subject_id = des_req['subject_id']
    subject = Subject.objects.get(id=subject_id)
    new_meeting = Meeting(author=author, title=title, description=description, location=location, max_member=max_member, subject=subject)
    new_meeting.save()
    new_meeting.members.add(*members)
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
      dict_meeting = model_to_dict(meeting)
      dict_meeting['members']=list(meeting.members.all().values())
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(dict_meeting)
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = User.objects.get(id=author_id)
    title = des_req['title']
    description = des_req['description']
    location = des_req['location']
    max_member = des_req['max_member']
    member_ids = des_req['member_ids']
    members = User.objects.filter(id__in=member_ids)
    subject_id = des_req['subject_id']
    subject = Subject.objects.get(id=subject_id)
    try:
      meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    meeting.author = author
    meeting.title = title
    meeting.description = description
    meeting.location = location
    meeting.max_member = max_member
    meeting.members.clear()
    meeting.members.add(*members)
    meeting.subject = subject
    meeting.save()
    return HttpResponse(status=204)
  elif request.method == 'DELETE':
    try:
      meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    meeting.delete()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['PUT'],['DELETE'])

# url: /meeting/:id/comment
def meetingComment(request, meeting_id):
  meeting_id = int(meeting_id)
  if request.method == 'GET':
    return JsonResponse(list(Meeting.objects.get(id=meeting_id).commentsMeeting.all().values()), safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = User.objects.get(id=author_id)
    meeting = Meeting.objects.get(id=meeting_id)
    content = des_req['content']
    publicity = des_req['publicity']
    new_comment = Comment(author=author, meeting=meeting, content=content, publicity=publicity)
    new_comment.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /comment
def commentList(request):
  if request.method == 'GET':
    return JsonResponse(list(Comment.objects.all().values()), safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = User.objects.get(id=author_id)
    meeting_id = des_req['meeting_id']
    meeting = Meeting.objects.get(id=meeting_id)
    content = des_req['content']
    publicity = des_req['publicity']
    new_comment = Comment(author=author, meeting=meeting, content=content, publicity=publicity)
    new_comment.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /comment/:id
def commentDetail(request, comment_id):
  comment_id = int(comment_id)
  if request.method == 'GET':
    try:
      comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(model_to_dict(comment))
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = User.objects.get(id=author_id)
    meeting_id = des_req['meeting_id']
    meeting = Meeting.objects.get(id=meeting_id)
    content = des_req['content']
    publicity = des_req['publicity']
    try:
      comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
      return HttpResponseNotFound()
    comment.author = author
    comment.meeting = meeting
    comment.content = content
    comment.publicity = publicity
    comment.save()
    return HttpResponse(status=204)
  elif request.method == 'DELETE':
    try:
      comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
      return HttpResponseNotFound()
    comment.delete()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['PUT'],['DELETE'])

# url: /subject
def subjectList(request):
  if request.method == 'GET':
    return JsonResponse(list(Subject.objects.all().values()), safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    interest = des_req['interest']
    name = des_req['name']
    new_subject = Subject(interest=interest, name=name)
    new_subject.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /subject/:id
def subjectDetail(request, subject_id):
  subject_id = int(subject_id)
  if request.method == 'GET':
    try:
      subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(model_to_dict(subject))
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    interest = des_req['interest']
    name = des_req['name']
    try:
      subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
      return HttpResponseNotFound()
    subject.interest = interest
    subject.name = name
    subject.save()
    return HttpResponse(status=204)
  elif request.method == 'DELETE':
    try:
      subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
      return HttpResponseNotFound()
    subject.delete()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['PUT'],['DELETE'])

# url: /college
def collegeList(request):
  if request.method == 'GET':
    return JsonResponse(list(College.objects.all().values()), safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    name = des_req['name']
    new_college = College(name=name)
    new_college.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /college/:id
def collegeDetail(request, college_id):
  college_id = int(college_id)
  if request.method == 'GET':
    try:
      college = College.objects.get(id=college_id)
    except College.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(model_to_dict(college))
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode()) # Deserialized request
    name = des_req['name']
    try:
      college = College.objects.get(id=college_id)
    except College.DoesNotExist:
      return HttpResponseNotFound()
    college.name = name
    college.save()
    return HttpResponse(status=204)
  elif request.method == 'DELETE':
    try:
      college = College.objects.get(id=college_id)
    except College.DoesNotExist:
      return HttpResponseNotFound()
    college.delete()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['PUT'],['DELETE'])
