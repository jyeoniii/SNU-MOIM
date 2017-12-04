from django.conf.urls import url, include
from .views import *

urlpatterns = [
  url('^token$', token, name='token'),
  url(r'^check_user$', check_user, name='check_user'),
  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
      activate, name='activate'),
  url(r'^activate_without_code', activate_without_code, name='activate_without_code'),
  url(r'^signup$', signup, name='signup'),
  url(r'^signin$', signin, name='signin'),
  url(r'^signout$', signout, name='signout'),
  url(r'^loginedUser$', loginedUser, name='loginedUser'),
  url(r'^user$', userList, name='userList'),
  url(r'^user/(?P<user_id>[0-9]+)$', userDetail, name='userDetail'),
  url(r'^meeting$', meetingList, name='meetingList'),
  url(r'^meeting/(?P<meeting_id>[0-9]+)$', meetingDetail, name='meetingDetail'),
  url(r'^meeting/(?P<meeting_id>[0-9]+)/comment$', meetingComment, name='meetingComment'),
  url(r'^comment$', commentList, name='commentList'),
  url(r'^comment/(?P<comment_id>[0-9]+)$', commentDetail, name='commentDetail'),
  url(r'^interest$', interestList, name='interestList'),
  url(r'^subject$', subjectList, name='subjectList'),
  url(r'^subject/(?P<subject_id>[0-9]+)$', subjectDetail, name='subjectDetail'),
  url(r'^college$', collegeList, name='collegeList'),
  url(r'^college/(?P<college_id>[0-9]+)$', collegeDetail, name='collegeDetail'),
  url(r'^message$', messageList, name='messageList'),
  url(r'^message/(?P<message_id>[0-9]+)$', messageDetail, name='messageDetail'),

  url(r'^meeting/search/title/(?P<query>.+)$', searchMeeting_title, name='searchMeeting_title'),
  url(r'^meeting/search/author/(?P<query>.+)$', searchMeeting_author, name='searchMeeting_author'),
  url(r'^meeting/search/subject/(?P<subject_id>[0-9]+)(_(?P<query>.+))?$', searchMeeting_subject, name='searchMeeting_subject'),
  url(r'^meeting/create$', meetingCreate, name='meetingCreate'),
  url(r'^meeting/(?P<meeting_id>[0-9]+)/edit$', meetingEdit, name='meetingEdit'),
  url(r'^joinMeeting/(?P<meeting_id>[0-9]+)$', joinMeeting, name='joinMeeting'),
  url(r'^leaveMeeting/(?P<meeting_id>[0-9]+)$', leaveMeeting, name='leaveMeeting'),
  url(r'^closeMeeting/(?P<meeting_id>[0-9]+)$', closeMeeting, name='closeMeeting'),
  url(r'^recommend/meeting/(?P<user_id>[0-9]+)/(?P<N>[0-9]+)$', recommendMeetings, name='recommendMeetings'),
  url(r'^messages$', get_django_messages, name='messages'),
  url(r'^add_message', add_django_message, name='add_messages')
]

