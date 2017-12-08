from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.messages import get_messages
from social_django.models import UserSocialAuth

from snumeeting.recommend.JoinHistoryManager import JoinHistoryManager
from snumeeting.recommend.computeRecommend import getRecMeetings, getUserSimilarity

import json
import datetime
import requests

from .tokens import account_activation_token
from .models import Ex_User, Meeting, Comment, Subject, College, Interest, Message
from .convert import convert_userinfo_for_front, convert_userinfo_minimal, convert_meeting_for_mainpage

import json
import requests

# url: /check_user
def check_user(request):
  if request.method == 'POST':
    username = json.loads(request.body.decode())['username']
    try:
      User.objects.get(username=username)
      return HttpResponse(status=409)
    except User.DoesNotExist:
      return HttpResponse(status=200)
  else:
    return HttpResponseNotAllowed(['POST'])

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
    user.is_active = False # this will be true after activation by email
    user.save()
    try: # these keys are only for testing
      access_token = req_data['access_token']
      fb_friend_ids = req_data['fb_friend_ids']
      fb_friends = Ex_User.objects.filter(id__in=fb_friend_ids)
    except KeyError:
      access_token = ''
      fb_friends=[]
    ex_User = Ex_User.objects.create(name=name, user=user, college=college, access_token=access_token) # create first, m2m later
    ex_User.save()
    ex_User.subjects.add(*subjects) # adding many-to-many at once
    ex_User.fb_friends.add(*fb_friends)
    ex_User.save()

    # Email Verification
    current_site = get_current_site(request)
    message = render_to_string('activation.html', {
      'user':user,
      'domain':current_site.domain,
      'uid': urlsafe_base64_encode(force_bytes(user.id)),
      'token': account_activation_token.make_token(user),
    })
    mail_subject = 'Activation mail for your SNU-moim account'
    email = EmailMessage(mail_subject, message, to=[email])
    email.send()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['POST'])

# url: /activiate_without_code
def activate_without_code(request):
  if request.method == 'PUT':
    username = json.loads(request.body.decode())['username']
    try:
      user = User.objects.get(username=username)
      user.is_active = True
      user.save()
      return HttpResponse(status=204)
    except User.DoesNotExist:
      return HttpResponseNotFound()
  else:
    return HttpResponseNotAllowed(['PUT'])


# url: /activate
def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
  except(User.DoesNotExist):
    return HttpResponseNotFound
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, 'Your account has been activated! Please sign in.')
    return redirect('http://localhost:4200/sign_in')
  else:
    return HttpResponse('The activation code has been expired. Please contact admin.', status=401)

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
      refresh_fb_friend_status(user)
      converted_user = convert_userinfo_for_front(user.id)
      return JsonResponse(converted_user, safe = False)
    else:
      return HttpResponse(status=401)
  else:
    return HttpResponseNotAllowed(['POST'])

def refresh_fb_friend_status(user):
  ex_user = Ex_User.objects.get(user=user)
  if ex_user.access_token != '' and ex_user.access_token != 'EXPIRED':
    url = 'https://graph.facebook.com/v2.11/me?fields=friends&access_token=' + ex_user.access_token
    response = requests.get(url)
    if (response.status_code == 400):
      ex_user.access_token = 'EXPIRED'
    elif (response.status_code == 200):
      friends = response.json()['friends']['data']

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
  ex_user = Ex_User.objects.get(user_id=request.user.id)
  return JsonResponse(convert_userinfo_for_front(ex_user.id), safe=False)

# url: /user
def userList(request):
  if request.method == 'GET':
    users = User.objects.all()
    dict_users = []
    for user in users:
      u = convert_userinfo_for_front(user.id)
      dict_users.append(u)
    return JsonResponse(dict_users, safe=False)
  else:
    return HttpResponseNotAllowed(['GET'])

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
      ex_user=Ex_User.objects.get(id=user_id)
      user = ex_user.user
    except Ex_User.DoesNotExist:
      return HttpResponseNotFound()
    user.set_password(password)
    user.save()
    ex_user.name = name
    ex_user.college = college
    ex_user.subjects.clear()
    ex_user.subjects.add(*subjects)
    ex_user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['PUT'])

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
    author = Ex_User.objects.get(id=int(author_id))
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
    commentsList = list(meeting.comments.all().values())
    for comment in commentsList:
      user = convert_userinfo_for_front(comment['author_id'])
      comment.pop('author_id')
      comment['author'] = user
    return JsonResponse(commentsList, safe=False)
  elif request.method == 'POST':
    des_req = json.loads(request.body.decode())
    author_id = des_req['author_id']
    author = Ex_User.objects.get(id=author_id)
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
    author = Ex_User.objects.get(id=author_id)
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
      for meeting in list(author.meetings_made.all()):
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
      meetings = subject.meetings.all()
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

# url: /message
def messageList(request):
  if request.method == 'GET':
    messagesList = list(Message.objects.all().values())
    for message in messagesList:
      sender = convert_userinfo_for_front(message['sender_id'])
      receiver = convert_userinfo_for_front(message['receiver_id'])
      message.pop('sender_id')
      message.pop('receiver_id')
      message['sender'] = sender
      message['receiver'] = receiver
    return JsonResponse(messagesList, safe=False)
  if request.method == 'POST':
    des_req = json.loads(request.body.decode())
    sender_id = des_req['sender_id']
    sender = Ex_User.objects.get(id=sender_id)
    receiver_id = des_req['receiver_id']
    receiver = Ex_User.objects.get(id=receiver_id)
    content = des_req['content']
    new_message = Message(sender=sender, receiver=receiver, content=content)
    new_message.save()
    now = datetime.datetime.now()

    sender = convert_userinfo_for_front(new_message.sender_id)
    receiver = convert_userinfo_for_front(new_message.receiver_id)
    message_dict = model_to_dict(new_message)
    message_dict['sender'] = sender
    message_dict['receiver'] = receiver
    message_dict['sended_at'] = now
    return JsonResponse(message_dict, status=201)
  else:
    return HttpResponseNotAllowed(['GET'],['POST'])

# url: /message/:id
def messageDetail(request, message_id):
  message_id = int(message_id)
  if request.method == 'GET':
    try:
      message = Message.objects.get(id=message_id)
      sender = convert_userinfo_for_front(message.sender_id)
      receiver = convert_userinfo_for_front(message.receiver_id)
      message_dict = model_to_dict(message)
      message_dict['sender'] = sender
      message_dict['receiver'] = receiver
    except Message.DoesNotExist:
      return HttpResponseNotFound()
    return JsonResponse(message_dict)
  elif request.method == 'DELETE':
    try:
      message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
      return HttpResponseNotFound()
    message.delete()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'],['DELETE'])

# url: /meeting/create
def meetingCreate(request):

  if request.method == 'POST':
    data = json.loads(request.body.decode())
    author_id = data['author_id']
    author = Ex_User.objects.get(id=author_id)
    title = data['title']
    description = data['description']
    location = data['location']
    max_member = data['max_member']
    # member_id = data['member_id']
    # member = User.objects.filter(id__in=member_id)
    subject_id = data['subject_id']
    subject = Subject.objects.get(id=subject_id)

    new_meeting = Meeting(
      author=author,
      title=title,
      description=description,
      location=location,
      max_member=max_member,
      subject=subject,
    )
    new_meeting.save()
    new_meeting.members.add(author)
    new_meeting.save()
    return HttpResponse(status=201)
  else:
    return HttpResponseNotAllowed(['POST'])


# url: /meeting/:id/edit
def meetingEdit(request, meeting_id):
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
    return JsonResponse(dict_meeting, safe = False);

  elif request.method == 'PUT':
    request = json.loads(request.body.decode())
    title = request['title']
    description = request['description']
    location = request['location']
    max_member = request['max_member']
    subject_id = request['subject_id']
    subject = Subject.objects.get(id= subject_id)
    try:
      meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()

    meeting.title = title
    meeting.description = description
    meeting.location = location
    meeting.max_member = max_member
    meeting.subject = subject
    meeting.save()
    return HttpResponse(status=204)

  else:
    return HttpResponseNotAllowed(['GET'],['PUT'])

# url: /joinMeeting/:meeting_id
def joinMeeting(request, meeting_id):
  if request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    user_id = des_req['user_id']
    try:
      meeting = Meeting.objects.get(id=meeting_id)
      if meeting.is_closed:
        return HttpResponseBadRequest()
      user = Ex_User.objects.get(id=user_id)
      meeting.members.add(user)
      manager = JoinHistoryManager()
      user.joinHistory = manager.increaseCnt(user.joinHistory, meeting.subject_id)
      user.college.joinHistory = manager.increaseCnt(user.college.joinHistory, meeting.subject_id)
      user.save()
      user.college.save()
      meeting.save()
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    except Ex_User.DoesNotExist:
      return HttpResponseNotFound()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['PUT'])

# url: /closeMeeting/:meeting_id
def closeMeeting(request, meeting_id):
  if request.method == 'GET':
    try:
      meeting = Meeting.objects.get(id=meeting_id)
      meeting.is_closed = True
      meeting.save()
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['GET'])

# url: /leaveMeeting/:meeting_id
def leaveMeeting(request, meeting_id):
  if request.method == 'PUT':
    des_req = json.loads(request.body.decode())
    user_id = des_req['user_id']
    try:
      meeting = Meeting.objects.get(id=meeting_id)
      if meeting.is_closed:
        return HttpResponseBadRequest()
      user = Ex_User.objects.get(id=user_id)
      manager = JoinHistoryManager()
      meeting.members.remove(user)
      user.joinHistory = manager.decreaseCnt(user.joinHistory, meeting.subject_id)
      user.college.joinHistory = manager.decreaseCnt(user.college.joinHistory, meeting.subject_id)
      user.save()
      user.college.save()
      meeting.save()
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
    except Ex_User.DoesNotExist:
      return HttpResponseNotFound()
    return HttpResponse(status=204)
  else:
    return HttpResponseNotAllowed(['PUT'])

def recommendMeetings(request, user_id, N):
  if request.method == 'GET':
    try:
      user = Ex_User.objects.get(id=int(user_id))
      result = getRecMeetings(user, int(N))
      return JsonResponse(result, safe=False)
    except Ex_User.DoesNotExist:
      return HttpResponseNotFound()
  else:
    return HttpResponseNotAllowed(['GET'])

# Recommend similar users to invite to the meeting
def recommendUsersForMeeting(request, user_id, meeting_id, N):
  if request.method == 'GET':
    try:
      result = [] 
      user = Ex_User.objects.get(id=int(user_id))
      meeting = Meeting.objects.get(id=meeting_id)
      uids = getUserSimilarity(user, int(N))

      for uid in uids:
        uid = uid[0]
        exist = False 
        for member in meeting.members.all():
          if uid == member.id: # Skip users who has already joined this meeting
            exist = True 
            break
        if not exist:
          recommendedUser = convert_userinfo_for_front(uid)
          result.append(recommendedUser)

      return JsonResponse(result, safe=False)
    except Ex_User.DoesNotExist:
      return HttpResponseNotFound()
    except Meeting.DoesNotExist:
      return HttpResponseNotFound()
 
  else:
    return HttpResponseNotAllowed(['GET'])


# Send Django message as JSON data.
# url: /messages
def get_django_messages(request):
  if request.method == 'GET':
    messages = get_messages(request)

    if len(messages) == 0:
      return HttpResponse(status=204)

    for message in messages:
      return JsonResponse({'message':message.message}, safe=False)
  else:
    return HttpResponseNotAllowed(['GET'])

# for testing
# url: /add_message
def add_django_message(request):
  if request.method == 'POST':
    req_data = json.loads(request.body.decode())
    messages.success(request, req_data['message'])
    return HttpResponse(status=200)
  else:
    return HttpResponseNotAllowed(['POST'])
