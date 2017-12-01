from snumeeting.models import Ex_User, College
from .JoinHistoryManager import JoinHistoryManager
import json

def SyncUserHistoryAll():
  users = Ex_User.objects.all()
  for user in users:
    ReinitUserHistory(user)

  #print("SyncUserHistoryAll() done")

def SyncCollegeHistoryAll():
  colleges = College.objects.all()
  for college in colleges:
    ReinitCollegeHistory(college)

  #print("SyncCollegeHistoryAll() done")

def ReinitUserHistory(user):
  manager = JoinHistoryManager()
  joinedMeetings = user.meetings_joined.all()
  jh = "{}"
  for meeting in joinedMeetings:
    subject_id = meeting.subject_id
    jh = manager.increaseCnt(jh, subject_id)
  user.joinHistory = jh
  user.save()

def ReinitCollegeHistory(college):
  manager = JoinHistoryManager()
  collegeMembers = college.users.all()
  jh = "{}"
  for user in collegeMembers:  # Iterate every college members
    joinedMeetings = user.meetings_joined.all()
    for meeting in joinedMeetings:
      subject_id = meeting.subject_id
      jh = manager.increaseCnt(jh, subject_id)
  college.joinHistory = jh
  college.save()

