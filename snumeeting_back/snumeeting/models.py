from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
  name = models.CharField(max_length=64)
  joinHistory = models.CharField(max_length=200, default='{}')

  def __str__(self):
    return self.name

class Interest(models.Model):
  name = models.CharField(max_length=64)

  def __str__(self):
    return self.name

class Subject(models.Model):
  name = models.CharField(max_length=64)
  interest = models.ForeignKey(
    Interest,
    on_delete=models.CASCADE,
    related_name='subjects',
    null=False
  )

  def __str__(self):
    return self.name

class Ex_User(models.Model):
  name = models.CharField(max_length=64)
  access_token = models.CharField(max_length=255)
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name = 'extended',
  )
  college = models.ForeignKey(
    College,
    on_delete=models.CASCADE,
    related_name = 'users',
    null=False
  )
  subjects = models.ManyToManyField(
    Subject,
    related_name = 'users',
  )
  fb_friends = models.ManyToManyField(
    'self',
  )
  joinHistory = models.CharField(max_length=200, default='{}')

  def __str__(self):
    return self.name

class Message(models.Model):
  sender = models.ForeignKey(
    Ex_User,
    related_name='messageSender',
    null=True
  )
  receiver = models.ForeignKey(
    Ex_User,
    related_name='messageReceiver',
    null=True
  )
  content = models.TextField()
  sended_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.content

class Meeting(models.Model):
  author = models.ForeignKey(
    Ex_User,
    on_delete=models.CASCADE,
    related_name='meetings_made',
    null=True
  )
  title = models.CharField(max_length=64)
  description = models.TextField()
  location = models.CharField(max_length=64)
  max_member = models.IntegerField()
  members = models.ManyToManyField(
    Ex_User,
    related_name = 'meetings_joined',
  )
  subject = models.ForeignKey(
    Subject,
    on_delete=models.CASCADE,
    related_name = 'meetings',
    null=True
  )
  is_closed= models.BooleanField(default=False)

  def __str__(self):
    return self.title

class Comment(models.Model):
  author = models.ForeignKey(
    Ex_User,
    on_delete=models.CASCADE,
    related_name='comments',
    null=True
  )
  meeting = models.ForeignKey(
    Meeting,
    on_delete=models.CASCADE,
    related_name='comments',
    null=True
  )
  content = models.CharField(max_length=64)
  publicity = models.BooleanField()

  def __str__(self):
    return self.content

