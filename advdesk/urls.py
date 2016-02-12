from django.conf.urls import patterns, include, url

urlpatterns = patterns('advdesk',



	url(r'^createadv/', 'views.createadv', name='createadv'),




	)