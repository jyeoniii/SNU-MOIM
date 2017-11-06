from django.test import TestCase, Client
from django.core import serializers
from django.contrib.auth.models import User
from .models import Ex_User, Meeting, Comment, Subject, College
from django.forms.models import model_to_dict
import json
import jsonpickle

class SnuMeetingTestCase(TestCase):
  def setUp(self):
    # College
    engineering = College.objects.create(id=0, name='Engineering')
    business = College.objects.create(id=1, name='Business')

    # Subject
    std_eng = Subject.objects.create(id=0, name='English', interest='study')
    std_chi = Subject.objects.create(id=1, name='Chinese', interest='study')
    pfm_band = Subject.objects.create(id=2, name='Band', interest='performance')

    # User
    fake1 = User.objects.create(id=0, username='fake1', password='1234', email='fake1@snu.ac.kr')
    fake2 = User.objects.create(id=1, username='fake2', password='1234', email='fake2@snu.ac.kr')
    fake3 = User.objects.create(id=2, username='fake3', password='1234', email='fake3@snu.ac.kr')
    fake1_ex = Ex_User.objects.create(id=0, user=fake1, college=engineering, subjects=[std_eng])
    fake2_ex = Ex_User.objects.create(id=1, user=fake2, college=business, subjects=[std_chi, pfm_band])
    fake3_ex = Ex_User.objects.create(id=2, user=fake3, college=business, subjects=[pfm_band])

    # Meeting
    meeting1 = Meeting.objects.create(id=0, author=fake1_ex, title='Study English',
      subject=std_eng, description='I will study English', location='SNUstation',
      max_member=4, members=[fake1_ex])
    meeting2 = Meeting.objects.create(id=1, author=fake2_ex, title='Study Chinese',
      subject=std_chi, description='I will study Chinese', location='SNU',
      max_member=5, members=[fake2_ex, fake1_ex])
    meeting3 = Meeting.objects.create(id=2, author=fake3_ex, title='Need my band',
      subject=pfm_band, description='I need all the sessions', location='Nokdu',
      max_member=6, members=[fake3_ex, fake1_ex, fake2_ex])
    meeting4 = Meeting.objects.create(id=3, author=fake3_ex, title='English Master',
      subject=std_eng, description='Mastering English is fun', location='SNU',
      max_member=3, members=[fake3_ex, fake1_ex, fake2_ex])

    # Comment
    comment1 = Comment.objects.create(id=0, author=fake1_ex, meeting=meeting3,
      content='Hi', publicity=True)
    comment2 = Comment.objects.create(id=1, author=fake1_ex, meeting=meeting2,
      content='Hello', publicity=True)
    comment3 = Comment.objects.create(id=2, author=fake2_ex, meeting=meeting1,
      content='Hiiiiii', publicity=True)
    comment4 = Comment.objects.create(id=3, author=fake2_ex, meeting=meeting2,
      content='Nooooooo', publicity=True)
    comment5 = Comment.objects.create(id=4, author=fake3_ex, meeting=meeting3,
      content='What?', publicity=True)

    self.client = Client()

  def test_csrf(self):
    # By default, csrf checks are disabled in test client
    # To test csrf protection we enforce csrf checks here
    college = College.objects.get(id=0)
    subjects = Subject.objects.all().values()
    client = Client(enforce_csrf_checks=True)
    response = client.post(
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 403) # Request without csrf token returns 403 response

    response = client.get('/api/token')
    csrftoken = response.cookies['csrftoken'].value # Get csrf token from cookie
    self.assertEqual(response.status_code, 204)

    response = client.post(
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
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

  def test_signup(self):
    # GET
    response = self.client.get('/api/signup')
    self.assertEqual(response.status_code, 405)

    # POST
    response = self.client.post(
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    # PUT
    response = self.client.put('/api/signup')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/signup')
    self.assertEqual(response.status_code, 405)

  def test_signin(self):
    # GET
    response = self.client.get('/api/signin')
    self.assertEqual(response.status_code, 405)

    # POST
    response = self.client.post( # Making fake user
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
      content_type='application/json',
    )
    response = self.client.post( # Correct email & password
      '/api/signin',
      json.dumps({'password':'test', 'mySNU':'test@snu.ac.kr'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 200)
    response = self.client.post( # Wrong password
      '/api/signin',
      json.dumps({'password':'wrong', 'mySNU':'test@snu.ac.kr'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 401)
    response = self.client.post( # Wrong email
      '/api/signin',
      json.dumps({'password':'test', 'mySNU':'wrong@snu.ac.kr'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 401)

    # PUT
    response = self.client.put('/api/signin')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/signin')
    self.assertEqual(response.status_code, 405)

  def test_signout(self):
    # GET
    response = self.client.post( # Making fake user
      '/api/signup',
      json.dumps({'name':'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
      content_type='application/json',
    )
    response = self.client.post( # Correct email & password
      '/api/signin',
      json.dumps({'password':'test', 'mySNU':'test@snu.ac.kr'}),
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

  def test_user_detail(self):
    # GET
    college = College.objects.get(id=0)
    subjects = list(Subject.objects.filter(id=0).all().values())
    response = self.client.get('/api/user/0')
    data = json.loads(response.content.decode())
#    self.assertEqual(data['username'], 'fake1')
#    self.assertEqual(data['user']['password'], '1234')
#    self.assertEqual(data['user']['email'], 'fake1@snu.ac.kr')
    self.assertEqual(data['college']['id'], 0)
    self.assertEqual(data['subjects'][0]['id'], 0)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/user/20') # Getting None-existing User
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/user/0')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put( # Editting user/0
      '/api/user/0',
      json.dumps({'name':'edit_test', 'password':'edit_test', 'mySNU':'test@snu.ac.kr', 'college_id':1, 'subject_ids':[1, 2]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    college = College.objects.get(id=1) # Test whether User and following Ex_User are updated
    subjects = list(Subject.objects.filter(id__in=[1, 2]).all().values())
    response = self.client.get('/api/user/0')
    data = json.loads(response.content.decode())
#    self.assertEqual(data['username'], fake1)
#    self.assertEqual(data['password'], 'edit_test')
#    self.assertEqual(data['email'], 'test@snu.ac.kr')
    self.assertEqual(data['college']['id'], 1)
    self.assertEqual(data['subjects'][0]['id'], 1)
    self.assertEqual(response.status_code, 200)

    response = self.client.put( # Editting None-existing User
      '/api/user/20',
      json.dumps({'name':'edit_test', 'password':'edit_test', 'mySNU':'test@snu.ac.kr', 'college_id':1, 'subject_ids':[1, 2]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/user/0') # Delete Existing User
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/user/0') # Delete None-existing User
    self.assertEqual(response.status_code, 404)

  def test_meeting_list(self):
    # GET
    response = self.client.get('/api/meeting')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['author']['id'], 0)
    self.assertEqual(data[0]['title'], 'Study English')
    self.assertEqual(data[0]['subject']['id'], 0)
    self.assertEqual(data[0]['description'], 'I will study English')
    self.assertEqual(data[0]['location'], 'SNUstation')
    self.assertEqual(data[0]['max_member'], 4)
    self.assertEqual(data[0]['members'][0]['id'], 0)
    self.assertEqual(len(data), 4)
    self.assertEqual(response.status_code, 200)
   
    # POST
    response = self.client.post(
      '/api/meeting',
      json.dumps({'author_id':2, 'title': 'Performance Band', 'subject_id':'2', 'description':'Who wants to get along with me?', 'location':'SNU', 'max_member':5, 'member_ids':[2, 1]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/meeting')
    data = json.loads(response.content.decode())
    self.assertEqual(data[4]['author']['id'], 2)
    self.assertEqual(data[4]['title'], 'Performance Band')
    self.assertEqual(data[4]['subject']['id'], 2)
    self.assertEqual(data[4]['description'], 'Who wants to get along with me?')
    self.assertEqual(data[4]['location'], 'SNU')
    self.assertEqual(data[4]['max_member'], 5)
    self.assertEqual(data[4]['members'][0]['id'], 2)
    self.assertEqual(len(data), 5)

    # PUT
    response = self.client.put('/api/meeting')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting')
    self.assertEqual(response.status_code, 405)

  def test_meeting_detail(self):
    # GET
    response = self.client.get('/api/meeting/0')
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 0)
    self.assertEqual(data['title'], 'Study English')
    self.assertEqual(data['subject']['id'], 0)
    self.assertEqual(data['description'], 'I will study English')
    self.assertEqual(data['location'], 'SNUstation')
    self.assertEqual(data['max_member'], 4)
    self.assertEqual(data['members'][0]['id'], 0)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/meeting/20') # Get None-existing Meeting
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/meeting/0')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put(
      '/api/meeting/0',
      json.dumps({'author_id':2, 'title': 'Performance Band', 'subject_id':'2', 'description':'Who wants to get along with me?', 'location':'SNU', 'max_member':5, 'member_ids':[2, 1]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.put(
      '/api/meeting/20',
      json.dumps({'author_id':2, 'title': 'Performance Band', 'subject_id':'2', 'description':'Who wants to get along with me?', 'location':'SNU', 'max_member':5, 'member_ids':[2, 1]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/meeting/0')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/meeting/0')
    self.assertEqual(response.status_code, 404)

  def test_meeting_comment(self):
    # GET
    response = self.client.get('/api/meeting/0/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['author']['id'], 1) 
    self.assertEqual(data[0]['meeting_id'], 0)
    self.assertEqual(data[0]['content'], 'Hiiiiii')
    self.assertEqual(data[0]['publicity'], True)
    self.assertEqual(len(data), 1)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/meeting/0/comment',
      json.dumps({'author_id':2, 'meeting_id':'0', 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/meeting/0/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[1]['author']['id'], 2)
    self.assertEqual(data[1]['meeting_id'], 0)
    self.assertEqual(data[1]['content'], 'New Comment')
    self.assertEqual(data[1]['publicity'], False)
    self.assertEqual(len(data), 2)

    # PUT
    response = self.client.put('/api/meeting/0/comment')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/meeting/0/comment')
    self.assertEqual(response.status_code, 405)

  def test_comment_list(self):
    # GET
    response = self.client.get('/api/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['author_id'], 0) 
    self.assertEqual(data[0]['meeting_id'], 2)
    self.assertEqual(data[0]['content'], 'Hi')
    self.assertEqual(data[0]['publicity'], True)
    self.assertEqual(len(data), 5)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/comment',
      json.dumps({'author_id':2, 'meeting_id':0, 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/comment')
    data = json.loads(response.content.decode())
    self.assertEqual(data[5]['author_id'], 2) 
    self.assertEqual(data[5]['meeting_id'], 0)
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
    response = self.client.get('/api/comment/0')
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 0) 
    self.assertEqual(data['meeting'], 2)
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
      '/api/comment/0',
      json.dumps({'author_id':2, 'meeting_id':0, 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.get('/api/comment/0') # Check the object is editted
    data = json.loads(response.content.decode())
    self.assertEqual(data['author']['id'], 0) 
    self.assertEqual(data['meeting'], 2)
    self.assertEqual(data['content'], 'New Comment')
    self.assertEqual(data['publicity'], False)

    response = self.client.put( # Edit None-existing Comment
      '/api/comment/20',
      json.dumps({'author_id':2, 'meeting_id':0, 'content':'New Comment', 'publicity':False}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/comment/0')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/comment/0') # Delete None-existing Comment
    self.assertEqual(response.status_code, 404)

  def test_subject_list(self):
    # GET
    response = self.client.get('/api/subject')
    data = json.loads(response.content.decode())
    self.assertEqual(data[0]['name'], 'English')
    self.assertEqual(data[0]['interest'], 'study')
    self.assertEqual(len(data), 3)
    self.assertEqual(response.status_code, 200)

    # POST
    response = self.client.post(
      '/api/subject',
      json.dumps({'name':'Dance', 'interest':'performance'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    response = self.client.get('/api/subject') # Check the object is created
    data = json.loads(response.content.decode())
    self.assertEqual(data[3]['name'], 'Dance')
    self.assertEqual(data[3]['interest'], 'performance')
    self.assertEqual(len(data), 4)

    # PUT
    response = self.client.put('/api/subject')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/subject')
    self.assertEqual(response.status_code, 405)

  def test_subject_detail(self):
    # GET
    response = self.client.get('/api/subject/0')
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'English')
    self.assertEqual(data['interest'], 'study')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/subject/20') # Get None-existing Subject
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/subject/0')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put(
      '/api/subject/0',
      json.dumps({'name':'Dance', 'interest':'performance'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.get('/api/subject/0') # Check the object is editted
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'Dance')
    self.assertEqual(data['interest'], 'performance')

    response = self.client.put( # Edit None-existing Subject
      '/api/subject/20',
      json.dumps({'name':'Dance', 'interest':'performance'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/subject/0')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/subject/0') # Delete None-existing Subject
    self.assertEqual(response.status_code, 404)

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
    response = self.client.get('/api/college/0')
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'Engineering')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/college/20') # Get None-existing College
    self.assertEqual(response.status_code, 404)

    # POST
    response = self.client.post('/api/college/0')
    self.assertEqual(response.status_code, 405)

    # PUT
    response = self.client.put(
      '/api/college/0',
      json.dumps({'name':'Literature'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 204)

    response = self.client.get('/api/college/0') # Check the object is editted
    data = json.loads(response.content.decode())
    self.assertEqual(data['name'], 'Literature')

    response = self.client.put( # Edit None-existing College
      '/api/college/20',
      json.dumps({'name':'Literature'}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 404)

    # DELETE
    response = self.client.delete('/api/college/0')
    self.assertEqual(response.status_code, 204)
    response = self.client.delete('/api/college/0') # Delete None-existing College
    self.assertEqual(response.status_code, 404)
