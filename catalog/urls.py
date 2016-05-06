from django.conf.urls import patterns, include, url

urlpatterns = patterns('catalog',
		url(r'^$', 'views.catalog', name='catalog'),


		)