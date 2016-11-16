from django.conf.urls import  include, url
from userprofile import views

urlpatterns = (
		# url(r'^inbox/$', 'views.inbox', name='inbox'),
		# url(r'^(?P<username>[0-9A-Za-z._%+-]+)/$', 'views.profile', name='profile'),
		url(r'^(?P<username>[0-9A-Za-z._%+-]+)/$', views.userprofile, name='userprofile'),


			   )