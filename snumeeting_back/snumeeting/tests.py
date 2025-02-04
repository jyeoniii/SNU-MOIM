from django.test import TestCase, Client
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from django.contrib import messages

from .models import Ex_User, Meeting, Comment, Subject, College, Interest, Message, Tag
from .social import check_user
from .convert import convert_userinfo_for_front, convert_userinfo_minimal, convert_meeting_for_mainpage

from snumeeting.recommend.JoinHistoryManager import JoinHistoryManager
from snumeeting.recommend.syncJoinHistory import *

import json

class SnuMeetingTestCase(TestCase):
  def setUp(self):

    # College
    engineering = College.objects.create(id=1, name='Engineering')
    business = College.objects.create(id=2, name='Business')

    # Interest
    int_study = Interest.objects.create(id=1, name='study')
    int_performance = Interest.objects.create(id=2, name='performance')

    # Subject
    std_eng = Subject.objects.create(id=1, name='English', interest=int_study)
    std_chi = Subject.objects.create(id=2, name='Chinese', interest=int_study)
    pfm_band = Subject.objects.create(id=3, name='Band', interest=int_performance)
    pfm_orc = Subject.objects.create(id=4, name='Orchestra', interest=int_performance)

    # User
    fake1 = User.objects.create(id=1, username='fake1', password='1234', email='fake1@snu.ac.kr')
    fake2 = User.objects.create(id=2, username='fake2', password='1234', email='fake2@snu.ac.kr')
    fake3 = User.objects.create(id=3, username='fake3', password='1234', email='fake3@snu.ac.kr')
    fake3_fb = UserSocialAuth.objects.create(user_id=3, uid=100407420743302, provider='facebook')
    fake1_ex = Ex_User.objects.create(id=1, user=fake1, name='John', college=engineering, subjects=[std_eng])
    fake2_ex = Ex_User.objects.create(id=2, user=fake2, name='Joshua',college=business, subjects=[std_chi, pfm_band])
    fake3_ex = Ex_User.objects.create(id=3, user=fake3, name='Alice', college=business, subjects=[pfm_band],
                                      fb_friends=[fake1_ex], access_token='EXPIRED')
    # Tag
    tag_study = Tag.objects.create(id=1, name='study')
    tag_english = Tag.objects.create(id=2, name='english')
    tag_urgent = Tag.objects.create(id=3, name='urgent')

    # Meeting
    meeting1 = Meeting.objects.create(id=1, author=fake1_ex, title='Study English',
                                      subject=std_eng, description='I will study English', location='SNUstation',
                                      max_member=4, members=[fake1_ex], tags=[tag_study, tag_english])
    meeting2 = Meeting.objects.create(id=2, author=fake2_ex, title='Study Chinese',
                                      subject=std_chi, description='I will study Chinese', location='SNU',
                                      max_member=5, members=[fake2_ex, fake1_ex], tags=[tag_study])
    meeting3 = Meeting.objects.create(id=3, author=fake3_ex, title='Need my band',
                                      subject=pfm_band, description='I need all the sessions', location='Nokdu',
                                      max_member=6, members=[fake3_ex, fake1_ex, fake2_ex], tags=[])
    meeting4 = Meeting.objects.create(id=4, author=fake3_ex, title='English Master',
                                      subject=std_eng, description='Mastering English is fun', location='SNU',
                                      max_member=3, members=[fake3_ex, fake1_ex, fake2_ex], tags=[tag_english])

    # Comment
    comment1 = Comment.objects.create(id=1, author=fake1_ex, meeting=meeting3,
                                      content='Hi', publicity=True)
    comment2 = Comment.objects.create(id=2, author=fake1_ex, meeting=meeting2,
                                      content='Hello', publicity=True)
    comment3 = Comment.objects.create(id=3, author=fake2_ex, meeting=meeting1,
                                      content='Hiiiiii', publicity=True)
    comment4 = Comment.objects.create(id=4, author=fake2_ex, meeting=meeting2,
                                      content='Nooooooo', publicity=True)
    comment5 = Comment.objects.create(id=5, author=fake3_ex, meeting=meeting3,
                                      content='What?', publicity=True)

    # Message
    message1 = Message.objects.create(id=1, sender=fake1_ex, receiver=fake3_ex,
      content='I want to join you')
    message2 = Message.objects.create(id=2, sender=fake2_ex, receiver=fake3_ex,
      content='I like your mo-im')
    message3 = Message.objects.create(id=3, sender=fake2_ex, receiver=fake1_ex,
      content='Who are you?')

    self.client = Client()

    self.manager = JoinHistoryManager()
    SyncUserHistoryAll()
    SyncCollegeHistoryAll()
 

  def test_csrf(self):
    # By default, csrf checks are disabled in test client
    # To test csrf protection we enforce csrf checks here
    college = College.objects.get(id=1)
    subjects = Subject.objects.all().values()
    client = Client(enforce_csrf_checks=True)
    response = client.post(
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'username':'test', 'college_id':1, 'subject_ids':[1]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 403) # Request without csrf token returns 403 response

    response = client.get('/api/token')
    csrftoken = response.cookies['csrftoken'].value # Get csrf token from cookie
    self.assertEqual(response.status_code, 204)

    response = client.post(
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'username':'test', 'college_id':1, 'subject_ids':[1]}),
      content_type='application/json',
      HTTP_X_CSRFTOKEN=csrftoken
    )
    self.assertEqual(response.status_code, 201) # Pass csrf protection

    response = client.post('/api/token', HTTP_X_CSRFTOKEN=csrftoken)
    self.assertEqual(response.status_code, 405)

    response = client.put('/api/token', HTTP_X_CSRFTOKEN=csrftoken)
    self.assertEqual(response.status_code, 405)

    response = client.delete('/api/token', HTTP_X_CSRFTOKEN=csrftoken)
    self.assertEqual(response.status_code, 405)

  def test_token(self):
    response = self.client.get('/api/token')
    self.assertEqual(response.status_code, 204)

    # Test token with wrong requests
    response = self.client.put('/api/token')
    self.assertEqual(response.status_code, 405)

  def test_model_str(self):
    # Test __str__ function of models
    college = College.objects.get(id=2)
    self.assertEqual(str(college), college.name)

    interest = Interest.objects.get(id=2)
    self.assertEqual(str(interest), interest.name)

    subject = Subject.objects.get(id=2)
    self.assertEqual(str(subject), subject.name)

    ex_user = Ex_User.objects.get(id=2)
    self.assertEqual(str(ex_user), ex_user.name)

    meeting = Meeting.objects.get(id=2)
    self.assertEqual(str(meeting), meeting.title)

    comment = Comment.objects.get(id=2)
    self.assertEqual(str(comment), comment.content)

    message = Message.objects.get(id=2)
    self.assertEqual(str(message), message.content)

    tag = Tag.objects.get(id=1)
    self.assertEqual(str(tag), tag.name)

  def test_check_user(self):
    # POST
    response = self.client.post('/api/check_user',
                                json.dumps({'username':'fake'}),
                                content_type='application/json')
    self.assertEqual(response.status_code, 200)

    response = self.client.post('/api/check_user',
                                json.dumps({'username':'fake1'}),
                                content_type='application/json')
    self.assertEqual(response.status_code, 409)

    # GET
    response = self.client.get('/api/check_user')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put('/api/check_user')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/check_user')
    self.assertEqual(response.status_code, 405)

  def test_signup(self):
    # GET
    response = self.client.get('/api/signup')
    self.assertEqual(response.status_code, 405)

    # POST
    response = self.client.post(
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'username':'test', 'college_id':1, 'subject_ids':[1]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    # PUT
    response = self.client.put('/api/signup')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/signup')
    self.assertEqual(response.status_code, 405)

  def test_activate_without_code_and_signin(self):
    # GET
    response = self.client.get('/api/signin')
    self.assertEqual(response.status_code, 405)

    # POST
    self.client.post( # Making fake user
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'username':'test', 'college_id':1, 'subject_ids':[1],
                  'access_token':'EAALMoP2WHT4BADFPbkwUY3Um3ZBBmmPJbA4ZBXdd8fCnmo4pyMprZAxZAMzVHFKdY8Fpb08trFMIVo2vNsgiCJUkW6iPHN7qre38lZCJxdVBTZAWrQNjli5VHTuY1CQ1M2T2ZBTq6HeRsOqgoOpDjy4sXKidhgf6Y5ydpDWGwQwXWaFAFR4uTf4',
                  'fb_friend_ids':[1]}),
      content_type='application/json',
    )

    self.client.put( # Activate the fake user without activation code
      '/api/activate_without_code',
      json.dumps({'username':'test'}),
      content_type='application/json',
    )

    self.client.post( # Making fake user with wrong FB access token
      '/api/signup',
      json.dumps({'name':'test1', 'password':'test1', 'username':'test1', 'college_id':1, 'subject_ids':[1],
                  'access_token':'wrong_token', 'fb_friend_ids':[3]
                  }),
      content_type='application/json',
    )

    self.client.put( # Activate the fake user without activation code
      '/api/activate_without_code',
      json.dumps({'username':'test1'}),
      content_type='application/json',
    )

    response = self.client.post( # Correct email & password
      '/api/signin',
      json.dumps({'password':'test', 'username':'test'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 200)

    response = self.client.post( # Correct email & password with wrong FB access token
      '/api/signin',
      json.dumps({'password':'test1', 'username':'test1'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 200)

    response = self.client.post( # Wrong password
      '/api/signin',
      json.dumps({'password':'wrong', 'username':'test'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 401)
    response = self.client.post( # Wrong email
      '/api/signin',
      json.dumps({'password':'test', 'username':'wrong'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 401)

    # Activate user who does not exist
    response = self.client.put(
      '/api/activate_without_code',
      json.dumps({'username':'testtest'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # PUT
    response = self.client.put('/api/signin')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/signin')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/activate_without_code',
      json.dumps({'username':'wrong'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 405)

  def test_signout(self):
    # GET
    response = self.client.post( # Making fake user
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'username':'test', 'college_id':1, 'subject_ids':[1]}),
      content_type='application/json',
    )
    response = self.client.post( # Correct email & password
      '/api/signin',
      json.dumps({'password':'test', 'username':'test'}),
      content_type='application/json',
    )
    response = self.client.get('/api/signout')
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post('/api/signout')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put('/api/signout')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/signout')
    self.assertEqual(response.status_code, 405)

  def test_user_list(self):
    # GET
    response = self.client.get('/api/user')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['username'], 'fake1')
    # self.assertEqual(data[0]['email'], 'fake1@snu.ac.kr')
    # self.assertEqual(data[0]['ex_User']['name'], 'John')
    self.assertEqual(len(data), 3)
    self.assertEqual(response.status_code, 200)
   
    # POST
    response = self.client.post('/api/user')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put('/api/user')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/user')
    self.assertEqual(response.status_code, 405)

  def test_user_detail(self):
    # GET
    college = College.objects.get(id=1)
    subjects = list(Subject.objects.filter(id=1).all().values())
    response = self.client.get('/api/user/1')
    data = json.loads(response.content.decode())
    #    self.assertEqual(data['username'], 'fake1')
    #    self.assertEqual(data['user']['password'], '1234')
    #    self.assertEqual(data['user']['email'], 'fake1@snu.ac.kr')
    self.assertEqual(data['college']['id'], 1)
    self.assertEqual(data['subjects'][0]['id'], 1)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/user/20') # Getting None-existing User
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/user/1')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put( # Editting user/0
            '/api/user/1',
      json.dumps({'name':'edit_test', 'password':'edit_test', 'username':'test', 'college_id':2, 'subject_ids':[2, 3]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    college = College.objects.get(id=2) # Test whether User and following Ex_User are updated
    subjects = list(Subject.objects.filter(id__in=[2, 3]).all().values())
    response = self.client.get('/api/user/1')
    data = json.loads(response.content.decode())
    #    self.assertEqual(data['username'], fake1)
    #    self.assertEqual(data['password'], 'edit_test')
    #    self.assertEqual(data['email'], 'test@snu.ac.kr')
    self.assertEqual(data['college']['id'], 2)
    self.assertEqual(data['subjects'][0]['id'], 2)
    self.assertEqual(response.status_code, 200)

    response = self.client.put( # Editting None-existing User
      '/api/user/20',
      json.dumps({'name':'edit_test', 'password':'edit_test', 'username':'test', 'college_id':1, 'subject_ids':[1, 2]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/user/1')
    self.assertEqual(response.status_code, 405)

  def test_meeting_list(self):
    # GET
    response = self.client.get('/api/meeting')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['author']['id'], 1)
    self.assertEqual(data[0]['title'], 'Study English')
    self.assertEqual(data[0]['subject']['id'], 1)
    self.assertEqual(data[0]['description'], 'I will study English')
    self.assertEqual(data[0]['location'], 'SNUstation')
    self.assertEqual(data[0]['max_member'], 4)
    self.assertEqual(data[0]['members'][0]['id'], 1)
    self.assertEqual(len(data), 4)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/meeting',
      json.dumps({'author_id':3, 'title': 'Performance Band', 'subject_id':'3', 'description':'Who wants to get along with me?', 'location':'SNU', 'max_member':5, 'member_ids':[2, 3], 'tag_names':['performance', 'band']}),
      content_type='application/json',
    )
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 3)
    self.assertEqual(data['title'], 'Performance Band')
    self.assertEqual(data['subject']['id'], 3)
    self.assertEqual(data['description'], 'Who wants to get along with me?')
    self.assertEqual(data['location'], 'SNU')
    self.assertEqual(data['max_member'], 5)
    self.assertEqual(data['members'][0]['id'], 3)

    # PUT
    response = self.client.put('/api/meeting')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting')
    self.assertEqual(response.status_code, 405)

  def test_meeting_detail(self):
    # GET
    response = self.client.get('/api/meeting/1')
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 1)
    self.assertEqual(data['title'], 'Study English')
    self.assertEqual(data['subject']['id'], 1)
    self.assertEqual(data['description'], 'I will study English')
    self.assertEqual(data['location'], 'SNUstation')
    self.assertEqual(data['max_member'], 4)
    self.assertEqual(data['members'][0]['id'], 1)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/meeting/20') # Get None-existing Meeting
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/meeting/0')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put(
      '/api/meeting/1',
      json.dumps({'author_id':3, 'title': 'Performance Band', 'subject_id':'3', 'description':'Who wants to get along with me?', 'location':'SNU', 'max_member':5, 'member_ids':[2, 3], 'tag_names':['performance', 'band']}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.put(
      '/api/meeting/20',
      json.dumps({'author_id':3, 'title': 'Performance Band', 'subject_id':'3', 'description':'Who wants to get along with me?', 'location':'SNU', 'max_member':5, 'member_ids':[2, 3], 'tag_names':['performance', 'band']}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/meeting/1')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/meeting/1')
    self.assertEqual(response.status_code, 404)

  def test_meeting_comment(self):
    # GET
    response = self.client.get('/api/meeting/1/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['author']['id'], 2)
    self.assertEqual(data[0]['meeting_id'], 1)
    self.assertEqual(data[0]['content'], 'Hiiiiii')
    self.assertEqual(data[0]['publicity'], True)
    self.assertEqual(len(data), 1)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/meeting/20/comment') # Get None-existing Meeting Comment
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post(
      '/api/meeting/1/comment',
      json.dumps({'author_id':3, 'meeting_id':'1', 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/meeting/1/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[1]['author']['id'], 3)
    self.assertEqual(data[1]['meeting_id'], 1)
    self.assertEqual(data[1]['content'], 'New Comment')
    self.assertEqual(data[1]['publicity'], False)
    self.assertEqual(len(data), 2)

    # PUT
    response = self.client.put('/api/meeting/1/comment')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting/1/comment')
    self.assertEqual(response.status_code, 405)

  def test_comment_list(self):
    # GET
    response = self.client.get('/api/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['author_id'], 1)
    self.assertEqual(data[0]['meeting_id'], 3)
    self.assertEqual(data[0]['content'], 'Hi')
    self.assertEqual(data[0]['publicity'], True)
    self.assertEqual(len(data), 5)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/comment',
      json.dumps({'author_id':3, 'meeting_id':1, 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[5]['author_id'], 3)
    self.assertEqual(data[5]['meeting_id'], 1)
    self.assertEqual(data[5]['content'], 'New Comment')
    self.assertEqual(data[5]['publicity'], False)
    self.assertEqual(len(data), 6)

    # PUT
    response = self.client.put('/api/comment')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/comment')
    self.assertEqual(response.status_code, 405)

  def test_comment_detail(self):
    # GET
    response = self.client.get('/api/comment/1')
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 1)
    self.assertEqual(data['meeting'], 3)
    self.assertEqual(data['content'], 'Hi')
    self.assertEqual(data['publicity'], True)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/comment/20') # Get None-existing Comment
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/comment/0')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put(
      '/api/comment/1',
      json.dumps({'author_id':3, 'meeting_id':1, 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.get('/api/comment/1') # Check the object is editted
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 1)
    self.assertEqual(data['meeting'], 3)
    self.assertEqual(data['content'], 'New Comment')
    self.assertEqual(data['publicity'], False)

    response = self.client.put( # Edit None-existing Comment
      '/api/comment/20',
      json.dumps({'author_id':2, 'meeting_id':1, 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/comment/1')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/comment/1') # Delete None-existing Comment
    self.assertEqual(response.status_code, 404)

  def test_interest_list(self):
    # GET
    response = self.client.get('/api/interest')
    data = json.loads(response.content.decode())
    self.assertEqual(len(data), 2)
    self.assertEqual(response.status_code, 200)

    # wrong request
    response = self.client.post('/api/interest')
    self.assertEqual(response.status_code, 405)


  def test_subject_list(self):
    # GET
    response = self.client.get('/api/subject')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['name'], 'English')
    self.assertEqual(data[0]['interest_id'], 1)
    self.assertEqual(len(data), 4)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/subject',
      json.dumps({'name':'Dance', 'interest_id':2}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/subject') # Check the object is created
    data = json.loads(response.content.decode())
    self.assertEqual(data[-1]['name'], 'Dance')
    self.assertEqual(data[-1]['interest_id'], 2)
    self.assertEqual(len(data), 5)

    # PUT
    response = self.client.put('/api/subject')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/subject')
    self.assertEqual(response.status_code, 405)

  def test_subject_detail(self):
    # GET
    response = self.client.get('/api/subject/1')
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'English')
    self.assertEqual(data['interest'], 1)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/subject/20') # Get None-existing Subject
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/subject/1')
    self.assertEqual(response.status_code, 405)

  def test_college_list(self):
    # GET
    response = self.client.get('/api/college')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['name'], 'Engineering')
    self.assertEqual(len(data), 2)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/college',
      json.dumps({'name':'Literature'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/college') # Check the object is created
    data = json.loads(response.content.decode())
    self.assertEqual(data[2]['name'], 'Literature')
    self.assertEqual(len(data), 3)

    # PUT
    response = self.client.put('/api/college')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/college')
    self.assertEqual(response.status_code, 405)

  def test_college_detail(self):
    # GET
    response = self.client.get('/api/college/1')
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'Engineering')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/college/20') # Get None-existing College
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/college/1')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put(
      '/api/college/1',
      json.dumps({'name':'Literature'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.get('/api/college/1') # Check the object is editted
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'Literature')

    response = self.client.put( # Edit None-existing College
      '/api/college/20',
      json.dumps({'name':'Literature'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/college/1')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/college/1') # Delete None-existing College
    self.assertEqual(response.status_code, 404)

  def test_search_meeting_title(self):
    # GET
    query = 'study'
    response = self.client.get('/api/meeting/search/title/'+query)
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 2)
    for meeting in result:
      self.assertTrue(query.lower() in meeting['title'].lower())

    # GET - no result
    query = 'xxx'
    response = self.client.get('/api/meeting/search/title/'+query)
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 0)

    # Not allowed HTTP request methods
    # PUT
    response = self.client.put('/api/meeting/search/title/'+query)
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting/search/title/'+query)
    self.assertEqual(response.status_code, 405)

    # POST
    response = self.client.post('/api/meeting/search/title/'+query)
    self.assertEqual(response.status_code, 405)


  def test_search_meeting_author(self):
    # GET
    query = 'jo'
    response = self.client.get('/api/meeting/search/author/'+query)
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 2)
    for meeting in result:
      self.assertTrue(query.lower() in meeting['author']['name'].lower())

    # GET - no result
    query = 'xxx'
    response = self.client.get('/api/meeting/search/author/'+query)
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 0)

    # Not allowed HTTP request methods
    # PUT
    response = self.client.put('/api/meeting/search/author/'+query)
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting/search/author/'+query)
    self.assertEqual(response.status_code, 405)

    # POST
    response = self.client.post('/api/meeting/search/author/'+query)
    self.assertEqual(response.status_code, 405)


  def test_search_meeting_subject(self):
    # GET
    subject_id = 1
    response = self.client.get('/api/meeting/search/subject/'+str(subject_id))
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 2)
    for meeting in result:
      self.assertEqual(meeting['subject']['id'], subject_id)

    # GET - no result
    subject_id = 4 
    response = self.client.get('/api/meeting/search/subject/'+str(subject_id))
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 0)

    # GET - non-existing subject
    subject_id = 10
    response = self.client.get('/api/meeting/search/subject/'+str(subject_id))
    self.assertEqual(response.status_code, 404)

    # GET - searching both for subject id and query
    subject_id = 1
    query = 'master'
    response = self.client.get('/api/meeting/search/subject/'+str(subject_id)+'_'+query)
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 1)
    for meeting in result:
      self.assertEqual(meeting['subject']['id'], subject_id)
      self.assertTrue(query.lower() in meeting['title'].lower())

    # Not allowed HTTP request methods
    # PUT
    response = self.client.put('/api/meeting/search/subject/'+str(subject_id))
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting/search/subject/'+str(subject_id))
    self.assertEqual(response.status_code, 405)

    # POST
    response = self.client.post('/api/meeting/search/subject/'+str(subject_id))
    self.assertEqual(response.status_code, 405)

  def test_convert_userinfo_for_front(self):
    user = convert_userinfo_for_front(1)
    self.assertEqual(user['id'],1)
    self.assertEqual(user['username'],'fake1')
    self.assertEqual(user['name'],'John')
    self.assertEqual(user['college']['name'],'Engineering')
    self.assertEqual(len(user['subjects']),1)

    # Non-existing user
    user = convert_userinfo_for_front(10)
    self.assertEqual(user['name'], 'NONEXISTING')

  def test_convert_userinfo_minimal(self):
    user = convert_userinfo_minimal(2)
    self.assertEqual(len(user), 2)
    self.assertEqual(user['id'],2)
    self.assertEqual(user['name'],'Joshua')

    # Non-existing user
    user = convert_userinfo_minimal(10)
    self.assertEqual(user['name'], 'NONEXISTING')

  def test_loginedUser(self):
    # No user logged in
    response = self.client.get('/api/loginedUser')
    result = json.loads(response.content.decode())
    self.assertEqual(result, None)

    # when user logged in
    self.client.post( # Making fake user
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'username':'test', 'college_id':1, 'subject_ids':[1]}),
      content_type='application/json',
    )
    self.client.put( # Activate the fake user without activation code
      '/api/activate_without_code',
      json.dumps({'username':'test'}),
      content_type='application/json',
    )
    self.client.post(
      '/api/signin',
      json.dumps({'username':'test', 'password':'test'}),
      content_type='application/json')

    response = self.client.get('/api/loginedUser')
    result = json.loads(response.content.decode())
    self.assertEqual(result['username'], 'test')
    self.assertEqual(result['name'], 'test')

    # No user logged in
    response = self.client.get('/api/loginedUser')
    result = json.loads(response.content.decode())
    self.assertEqual(result['username'], 'test')
    self.assertEqual(result['name'], 'test')
    
   
  def test_message_list(self):
    # GET
    response = self.client.get('/api/message')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['sender']['id'], 1) 
    self.assertEqual(data[0]['receiver']['id'], 3)
    self.assertEqual(data[0]['content'], 'I want to join you')
    self.assertEqual(len(data), 3)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/message',
      json.dumps({'sender_id':3, 'receiver_id':2, 'content':'Oh, I like it'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/message')
    data = json.loads(response.content.decode())
    self.assertEqual(data[3]['sender']['id'], 3) 
    self.assertEqual(data[3]['receiver']['id'], 2)
    self.assertEqual(data[3]['content'], 'Oh, I like it')
    self.assertEqual(len(data), 4)

    # PUT
    response = self.client.put('/api/message')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/message')
    self.assertEqual(response.status_code, 405)


  def test_message_detail(self):
    # GET
    response = self.client.get('/api/message/1')
    data = json.loads(response.content.decode())
    self.assertEqual(data['sender']['id'], 1)
    self.assertEqual(data['receiver']['id'], 3)
    self.assertEqual(data['content'], 'I want to join you')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/message/20') # Get None-existing Message
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/message/1')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put('/api/message/1')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/message/1')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/message/1') # Delete None-existing Message
    self.assertEqual(response.status_code, 404)

  def test_joinMeeting(self):
    meeting = Meeting.objects.get(id=2)
    user = Ex_User.objects.get(id=3)

    userjh_before = self.manager.getCount(user.joinHistory, meeting.subject.id)
    collegejh_before = self.manager.getCount(user.college.joinHistory, meeting.subject.id)
    len_before = len(meeting.members.all())

    response = self.client.put('/api/joinMeeting/2', json.dumps({'user_id':3}), content_type='application/json')

    user = Ex_User.objects.get(id=3)

    userjh_after = self.manager.getCount(user.joinHistory, meeting.subject.id)
    collegejh_after = self.manager.getCount(user.college.joinHistory, meeting.subject.id)
    len_after = len(meeting.members.all())

    self.assertEqual(userjh_before+1, userjh_after)
    self.assertEqual(collegejh_before+1, collegejh_after)
    self.assertEqual(len_before+1, len_after)

    # Non existing meeting
    response = self.client.put('/api/joinMeeting/10', json.dumps({'user_id':2}), content_type='application/json')
    self.assertEqual(response.status_code, 404)

    # Non existing user
    response = self.client.put('/api/joinMeeting/1', json.dumps({'user_id':12}), content_type='application/json')
    self.assertEqual(response.status_code, 404)

    # Not allowed methods
    response = self.client.get('/api/joinMeeting/1')
    self.assertEqual(response.status_code, 405)

    response = self.client.post('/api/joinMeeting/1')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/joinMeeting/1')
    self.assertEqual(response.status_code, 405)

  def test_leaveMeeting(self):
    meeting = Meeting.objects.get(id=2)
    user = Ex_User.objects.get(id=1)

    userjh_before = self.manager.getCount(user.joinHistory, meeting.subject.id)
    collegejh_before = self.manager.getCount(user.college.joinHistory, meeting.subject.id)
    len_before = len(meeting.members.all())

    response = self.client.put('/api/leaveMeeting/2', json.dumps({'user_id':1}), content_type='application/json')

    user = Ex_User.objects.get(id=1)
    userjh_after = self.manager.getCount(user.joinHistory, meeting.subject.id)
    collegejh_after = self.manager.getCount(user.college.joinHistory, meeting.subject.id)
    len_after = len(meeting.members.all())

    self.assertEqual(userjh_before-1, userjh_after)
    self.assertEqual(collegejh_before-1, collegejh_after)
    self.assertEqual(len_before-1, len_after)

    # User hasn't joined the meeting - Bad request
    response = self.client.put('/api/leaveMeeting/2', json.dumps({'user_id':3}), content_type='application/json')

    self.assertEqual(response.status_code, 400)

    # Non existing meeting
    response = self.client.put('/api/leaveMeeting/10', json.dumps({'user_id':2}), content_type='application/json')
    self.assertEqual(response.status_code, 404)

    # Non existing user
    response = self.client.put('/api/leaveMeeting/1', json.dumps({'user_id':12}), content_type='application/json')
    self.assertEqual(response.status_code, 404)

    # Not allowed methods
    response = self.client.get('/api/leaveMeeting/1')
    self.assertEqual(response.status_code, 405)

    response = self.client.post('/api/leaveMeeting/1')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/leaveMeeting/1')
    self.assertEqual(response.status_code, 405)

  def test_closeMeeting(self):
    response = self.client.get('/api/closeMeeting/4')
    response = self.client.get('/api/meeting/4')
    result = json.loads(response.content.decode())
    self.assertTrue(result['is_closed'])

    # Non existing meeting
    response = self.client.get('/api/closeMeeting/10')
    self.assertEqual(response.status_code, 404)

    # Not allowed methods
    response = self.client.put('/api/closeMeeting/1')
    self.assertEqual(response.status_code, 405)

    response = self.client.post('/api/closeMeeting/1')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/closeMeeting/1')
    self.assertEqual(response.status_code, 405)

  def test_django_messages(self):
    # No message
    response = self.client.get('/api/messages')
    self.assertEqual(response.status_code, 204)

    # Add message & get it
    response = self.client.post('/api/add_message', json.dumps({'message':'message'}), content_type='application/json')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/messages')
    self.assertEqual(response.status_code, 200)

    #PUT
    response = self.client.put('/api/messages')
    self.assertEqual(response.status_code, 405)

    response = self.client.put('/api/add_message')
    self.assertEqual(response.status_code, 405)

    #DELETE
    response = self.client.delete('/api/messages')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/add_message')
    self.assertEqual(response.status_code, 405)

  def test_tag_list(self):
    response = self.client.get('/api/tags')
    result = json.loads(response.content.decode())
    self.assertEqual(len(result),3)

    response = self.client.put('/api/tags')
    self.assertEqual(response.status_code, 405)

    response = self.client.post('/api/tags')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/tags')
    self.assertEqual(response.status_code, 405)

  def test_meetings_on_tag(self):
    response = self.client.get('/api/meeting/tag/study')
    result = json.loads(response.content.decode())
    self.assertEqual(len(result),2)

    response = self.client.put('/api/tags')
    self.assertEqual(response.status_code, 405)

    response = self.client.post('/api/tags')
    self.assertEqual(response.status_code, 405)

    response = self.client.delete('/api/tags')
    self.assertEqual(response.status_code, 405)

  def test_joinhistory_convert_to_list(self):
    user = Ex_User.objects.get(id=1)
    result = self.manager.convertToList(user.joinHistory)
    self.assertEqual(result, [2,1,1,0])

  def test_get_joined_meeting(self):
    user_id = 1
    response = self.client.get('/api/user/'+str(user_id)+'/meeting')
    result = json.loads(response.content.decode())

    self.assertEqual(len(result), 4)

    for m in result:
      result = False
      for member in m['members']:
        if user_id == member['id']:
          result = True
      self.assertEqual(result, True)

    # Method not allowed
    response = self.client.post('/api/user/'+str(user_id)+'/meeting')
    self.assertEqual(response.status_code, 405)

    # Method not allowed
    response = self.client.put('/api/user/'+str(user_id)+'/meeting')
    self.assertEqual(response.status_code, 405)

    # Method not allowed
    response = self.client.delete('/api/user/'+str(user_id)+'/meeting')
    self.assertEqual(response.status_code, 405)

    # Non existing user
    user_id = 10
    response = self.client.get('/api/user/'+str(user_id)+'/meeting')
    self.assertEqual(response.status_code, 404)






