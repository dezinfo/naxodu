from django.conf.urls import patterns, include, url

urlpatterns = patterns('userprofile',
		# url(r'^inbox/$', 'views.inbox', name='inbox'),
		# url(r'^(?P<username>[0-9A-Za-z._%+-]+)/$', 'views.profile', name='profile'),
		url(r'^(?P<username>[0-9A-Za-z._%+-]+)/$', 'views.userprofile', name='userprofile'),


		)