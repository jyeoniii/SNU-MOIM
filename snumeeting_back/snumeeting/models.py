from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
  name = models.CharField(max_length=64)

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
          related_name='subjects',
          null=False
          )

  def __str__(self):
    return self.name

class Ex_User(models.Model):
  name = models.CharField(max_length=64)
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name = 'extendedUser',
  )
  college = models.ForeignKey(
    College,
    related_name = 'usersCollege',
    null=False
  )
  subjects = models.ManyToManyField(
    Subject,
    related_name = 'usersSubjects',
  )
  fb_friends = models.ManyToManyField(
    'self',
    related_name = 'fbFriends'
  )

  def __str__(self):
    return self.name

class Meeting(models.Model):
  author = models.ForeignKey(
    Ex_User,
    related_name='meetingsAuthor',
    null=True
  )
  title = models.CharField(max_length=64)
  description = models.TextField()
  location = models.CharField(max_length=64)
  max_member = models.IntegerField()
  members = models.ManyToManyField(
    Ex_User,
    related_name = 'meetingsMembers',
  )
  subject = models.ForeignKey(
    Subject,
    related_name = 'meetingsSubject',
    null=True
  )

  def __str__(self):
    return self.title

class Comment(models.Model):
  author = models.ForeignKey(
    Ex_User,
    related_name='commentsAuthor',
    null=True
  )
  meeting = models.ForeignKey(
    Meeting,
    related_name='commentsMeeting',
    null=True
  )
  content = models.CharField(max_length=64)
  publicity = models.BooleanField()

  def __str__(self):
    return self.content

