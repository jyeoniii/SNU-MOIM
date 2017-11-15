from django.conf.urls import url, include
from .views import signup, signin, signout, userDetail
from .views import meetingList, meetingDetail, meetingComment, commentList, commentDetail
from .views import interestList, subjectList, subjectDetail, collegeList, collegeDetail
from .views import token
from .views import searchMeeting_title, searchMeeting_author, searchMeeting_subject

urlpatterns = [
  url('^token$', token, name='token'),
  url(r'^signup$', signup, name='signup'),
  url(r'^signin$', signin, name='signin'),
  url(r'^signout$', signout, name='signout'),
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

  url(r'^meeting/search/title/(?P<query>.+)$', searchMeeting_title, name='searchMeeting_title'),
  url(r'^meeting/search/author/(?P<query>.+)$', searchMeeting_author, name='searchMeeting_author'),
  url(r'^meeting/search/subject/(?P<subject_id>[0-9]+)(_(?P<query>.+))?$', searchMeeting_subject, name='searchMeeting_subject'),
]

