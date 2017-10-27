from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
  name = models.CharField(max_length=64)

class Ex_User(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  college = models.ForeignKey(
    College,
    related_name = 'users',
    null=True
  )

class Subject(models.Model):
  interest = models.CharField(max_length=64)
  name = models.CharField(max_length=64)
  users = models.ManyToManyField(
    Ex_User,
    related_name = 'subjects',
  )

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
