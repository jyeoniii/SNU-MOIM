from django.test import TestCase, Client
from .models import Ex_User, Meeting, Comment, Subject, College
from django.forms.models import model_to_dict

class SnuMeetingTestCase(TestCase):
  def setUp(self):
    # College
    engineering = College.objects.create(name='Engineering')
    business = College.objects.create(name='Business')

    # Subject
    std_eng = Subject.objects.create(name='English', interest: 'study')
    std_chi = Subject.objects.create(name='Chinese', interest: 'study')
    pfm_band = Subject.objects.create(name='Band', interest: 'performance')

    # User
    fake1 = Ex_User.objects.create(mySNU='fake1@snu.ac.kr', password='1234',
      name='fake1', college=engineering, interest=[std_eng])
    fake2 = Ex_User.objects.create(mySNU='fake2@snu.ac.kr', password='1234',
      name='fake2', college=business, interest=[std_chi, pfm_band])
    fake3 = Ex_User.objects.create(mySNU='fake3@snu.ac.kr', password='1234',
      name='fake3', college=business, interest=[pfm_band])

    # Meeting
    meeting1 = Meeting.objects.create(author=fake1, title='Study English', subject=std_eng,
      description='I will study English', location='SNUstation',
      max_member=4, members=[fake1])
    meeting2 = Meeting.objects.create(author=fake2, title='Study Chinese', subject=std_chi,
      description='I will study Chinese', location='SNU',
      max_member=5, members=[fake2, fake1])
    meeting3 = Meeting.objects.create(author=fake3, title='Need my band', subject=pfm_band,
      description='I need all the sessions', location='Nokdu',
      max_member=6, members=[fake3, fake1, fake2])
    meeting4 = Meeting.objects.create(author=fake3, title='English Master', subject=std_eng,
      description='Mastering English is fun', location='SNU',
      max_member=3, members=[fake3, fake1, fake2])

    # Comment
    comment1 = Comment.objects.create(author=fake1, meeting=meeting3,
      content='Hi', publicity=True)
    comment2 = Comment.objects.create(author=fake1, meeting=meeting2,
      content='Hello', publicity=True)
    comment3 = Comment.objects.create(author=fake2, meeting=meeting1,
      content='Hiiiiii', publicity=True)
    comment4 = Comment.objects.create(author=fake2, meeting=meeting2,
      content='Nooooooo', publicity=True)
    comment5 = Comment.objects.create(author=fake3, meeting=meeting3,
      content='What?', publicity=True)
