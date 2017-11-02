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
    fake1User = User.objects.create(id=0, username='fake1', password='1234', email='fake1@snu.ac.kr')
    fake2User = User.objects.create(id=1, username='fake2', password='1234', email='fake2@snu.ac.kr')
    fake3User = User.objects.create(id=2, username='fake3', password='1234', email='fake3@snu.ac.kr')
    fake1 = Ex_User.objects.create(id=0, user=fake1User, college=engineering, subjects=[std_eng])
    fake2 = Ex_User.objects.create(id=1, user=fake2User, college=business, subjects=[std_chi, pfm_band])
    fake3 = Ex_User.objects.create(id=2, user=fake3User, college=business, subjects=[pfm_band])

    # Meeting
    meeting1 = Meeting.objects.create(id=0, author=fake1, title='Study English',
      subject=std_eng, description='I will study English', location='SNUstation',
      max_member=4, members=[fake1])
    meeting2 = Meeting.objects.create(id=1, author=fake2, title='Study Chinese',
      subject=std_chi, description='I will study Chinese', location='SNU',
      max_member=5, members=[fake2, fake1])
    meeting3 = Meeting.objects.create(id=2, author=fake3, title='Need my band',
      subject=pfm_band, description='I need all the sessions', location='Nokdu',
      max_member=6, members=[fake3, fake1, fake2])
    meeting4 = Meeting.objects.create(id=3, author=fake3, title='English Master',
      subject=std_eng, description='Mastering English is fun', location='SNU',
      max_member=3, members=[fake3, fake1, fake2])

    # Comment
    comment1 = Comment.objects.create(id=0, author=fake1, meeting=meeting3,
      content='Hi', publicity=True)
    comment2 = Comment.objects.create(id=1, author=fake1, meeting=meeting2,
      content='Hello', publicity=True)
    comment3 = Comment.objects.create(id=2, author=fake2, meeting=meeting1,
      content='Hiiiiii', publicity=True)
    comment4 = Comment.objects.create(id=3, author=fake2, meeting=meeting2,
      content='Nooooooo', publicity=True)
    comment5 = Comment.objects.create(id=4, author=fake3, meeting=meeting3,
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
      json.dumps({'name': 'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 403) # Request without csrf token returns 403 response

    response = client.get('/api/token')
    csrftoken = response.cookies['csrftoken'].value # Get csrf token from cookie
    self.assertEqual(response.status_code, 204)

    response = client.post(
      '/api/signup',
      json.dumps({'name': 'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
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
    client = Client()

    # GET
    response = self.client.get('/api/signup')
    self.assertEqual(response.status_code, 405)

    # POST
    response = client.post(
      '/api/signup',
      json.dumps({'name': 'test', 'password':'test', 'mySNU':'test@snu.ac.kr', 'college_id':0, 'subject_ids':[0]}),
      content_type='application/json',
    )
    self.assertEqual(response.status_code, 201)

    # PUT
    response = self.client.put('/api/signup')
    self.assertEqual(response.status_code, 405)

    # DELETE
    response = self.client.delete('/api/signup')
    self.assertEqual(response.status_code, 405)


