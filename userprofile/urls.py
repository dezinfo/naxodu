from django.conf.urls import patterns, include, url

urlpatterns = patterns('userprofile',
		url(r'^inbox/$', 'views.inbox', name='inbox'),


		)