from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews',
		url(r'^$', 'views.reviews', name='reviews'),


		)