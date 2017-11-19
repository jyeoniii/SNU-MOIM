from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict
from .models import Ex_User, Meeting, Comment, Subject, College, Interest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
import json
from .convert import convert_userinfo_for_front, convert_userinfo_minimal, convert_meeting_for_mainpage

# url: /signup
def signup(request):
  if request.method == 'POST':
    req_data = json.loads(request.body.decode())
    name = req_data['name']
    username = req_data['username']
    password = req_data['password']
    email = req_data['username'] + '@snu.ac.kr'
    college_id = req_data['college_id'] # instead of getting object, gets id first
    college = College.objects.get(id=college_id) # gets the object by id
    subject_ids = req_data['subject_ids']
    subjects = Subject.objects.filter(id__in=subject_ids) # gets the objects by ids
    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    ex_User = Ex_User.objects.create(name=name, user=user, college=college) # create first, m2m later
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
    username = req_data['username']
    password = req_data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      converted_user = convert_userinfo_for_front(user.id)
      return JsonResponse(converted_user, safe = False)
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

def loginedUser(request):
  if request.user.is_anonymous:
    return JsonResponse(None, safe=False)
  return JsonResponse(convert_userinfo_for_front(request.user.id), safe=False)


# url: /user/:id
def userDetail(request, user_id):
  user_id = int(user_id)
  if request.method == 'GET':
    user = convert_userinfo_for_front(user_id)
    if user['name'] == 'NONEXISTING':
      return HttpResponseNotFound()
    return JsonResponse(user, safe = False)
  elif request.method == 'PUT':
    req_data = json.loads(request.body.decode())
    name = req_data['name']
    password = req_data['password']
    college_id = req_data['college_id'] # instead of getting object, gets id first
    college = College.objects.get(id=college_id) # gets the object by id
    subject_ids = req_data['subject_ids']
    subjects = Subject.objects.filter(id__in=subject_ids) # gets the objects by ids
    try:
      user = User.objects.get(id=user_id)
      ex_user=Ex_User.objects.get(user=user)
    except User.DoesNotExist:
      return HttpResponseNotFound()
    user.set_password(password)
    user.save()
    ex_user.user = user
    ex_user.name = name
    ex_user.college = college
    ex_user.subjects.clear()
    ex_user.subjects.add(*subjects)
    ex_user.save()
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
      d = convert_meeting_for_mainpage(meeting)
      dict_meetings.append(d)
    return JsonResponse(dict_meetings, safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())

    author_id = des_req['author_id']
    author = Ex_User.objects.get(user_id=int(author_id))
    title = des_req['title']
    description = des_req['description']
    location = des_req['location']
    max_member = des_req['max_member']
    #    member_ids = des_req['member_ids']
    #    members = User.objects.filter(id__in=member_ids)
    subject_id = des_req['subject_id']
    subject = Subject.objects.get(id=subject_id)

    # TODO: replace author -> request.user
    new_meeting = Meeting(author=author, title=title, description=description, location=location, max_member=max_member, subject=subject)
    new_meeting.save()
    new_meeting.members.add(author)
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

      author_id = dict_meeting['author']
      user = convert_userinfo_for_front(author_id)
      dict_meeting['author'] = user

      dict_meeting['members']=list(meeting.members.all().values())
      subject_id = dict_meeting['subject']
      dict_meeting['subject'] = model_to_dict(Subject.objects.get(id=subject_id))
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(dict_meeting)
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    title = des_req['title']
    description = des_req['description']
    location = des_req['location']
    max_member = des_req['max_member']
    #    member_ids = des_req['member_ids']
    #    members = User.objects.filter(id__in=member_ids)
    subject_id = des_req['subject_id']
    subject = Subject.objects.get(id=subject_id)
    try:
      meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    meeting.title = title
    meeting.description = description
    meeting.location = location
    meeting.max_member = max_member
    #    meeting.members.clear()
    #    meeting.members.add(*members)
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
    try:
      meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    commentsList = list(meeting.commentsMeeting.all().values())
    for comment in commentsList:
      user = convert_userinfo_for_front(comment['author_id'])
      comment.pop('author_id')
      comment['author'] = user
    return JsonResponse(commentsList, safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = Ex_User.objects.get(user_id=author_id)
    meeting = Meeting.objects.get(id=meeting_id)
    content = des_req['content']
    publicity = des_req['publicity']
    # TODO: replace author -> request.user
    new_comment = Comment(author=author, meeting=meeting, content=content, publicity=publicity)
    new_comment.save()

    comment_resp = model_to_dict(new_comment)
    author_front = convert_userinfo_for_front(author_id)
    comment_resp['author'] = author_front
    return JsonResponse(comment_resp, status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /comment
def commentList(request):
  if request.method == 'GET':
    return JsonResponse(list(Comment.objects.all().values()), safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = Ex_User.objects.get(user_id=author_id)
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
      user = convert_userinfo_for_front(comment.author_id)
      comment_dict = model_to_dict(comment)
      comment_dict['author'] = user
    except Comment.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(comment_dict)
  elif request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    content = des_req['content']
    publicity = des_req['publicity']
    try:
      comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
      return HttpResponseNotFound()
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
    interest_id = des_req['interest_id']
    interest = Interest.objects.get(id=interest_id)
    name = des_req['name']
    new_subject = Subject(interest=interest, name=name)
    new_subject.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

    # url: /interest
def interestList(request):
  if request.method == 'GET':
    interests = Interest.objects.all()
    dict_interests = []
    for interest in interests:
      d = model_to_dict(interest)
      d['subjects'] = list(interest.subjects.all().values())
      dict_interests.append(d)
    return JsonResponse(dict_interests, safe=False)
  else:
    return HttpResponseNotAllowed(['GET'])

# url: /subject/:id
def subjectDetail(request, subject_id):
  subject_id = int(subject_id)
  if request.method == 'GET':
    try:
      subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(model_to_dict(subject))
  else:
    return HttpResponseNotAllowed(['GET'])

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

# url: /meeting/search/title/:query
def searchMeeting_title(request, query):
  if request.method == 'GET':
    meetings = Meeting.objects.filter(Q(title__icontains=query))
    result = []
    for meeting in meetings:
      d = convert_meeting_for_mainpage(meeting)
      result.append(d)
  else:
    return HttpResponseNotAllowed(['GET'])
  return JsonResponse(result, safe=False) 

# url: /meeting/search/author/:query
def searchMeeting_author(request, query):
  if request.method == 'GET':
    result = []
    authors = Ex_User.objects.filter(Q(name__icontains=query))

    for author in authors:
      for meeting in list(author.meetingsAuthor.all()):
        d = convert_meeting_for_mainpage(meeting)
        result.append(d)
  else:
    return HttpResponseNotAllowed(['GET'])
  return JsonResponse(result, safe=False) 

# url: /meeting/search/author/:subject_id
#  or  /meeting/search/author/:subject_id_:query
def searchMeeting_subject(request, subject_id, query):
  if request.method == 'GET':
    result = []
    subject_id = int(subject_id)
    try:
      subject = Subject.objects.get(id=subject_id)
      meetings = subject.meetingsSubject.all()
      if query is not None:
        meetings = meetings.filter(Q(title__icontains=query))
      for meeting in meetings:
        d = convert_meeting_for_mainpage(meeting)
        result.append(d)
    except Subject.DoesNotExist:  # Non-existing subject
      return HttpResponseNotFound()
  else:
    return HttpResponseNotAllowed(['GET'])

  return JsonResponse(result, safe=False)

def joinMeeting(request):
  if request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    meeting_id = des_req['meeting_id']
    user_id = des_req['user_id']
    try:
      meeting = Meeting.objects.get(id=meeting_id)
      user = Ex_User.objects.get(id=user_id)
      meeting.members.add(user)
      meeting.save()
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    except Ex_User.DoesNotExist:
      return HttpResponseNotFound()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['PUT'])

