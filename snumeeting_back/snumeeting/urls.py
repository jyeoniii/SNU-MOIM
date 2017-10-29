from django.conf.urls import url, include
from .views import signup, signin, signout

urlpatterns = [
  url(r'^signup$', signup, name='singup'),
  url(r'^signin$', signin, name='singin'),
  url(r'^signout$', signout, name='singout'),
]
