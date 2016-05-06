from django.conf.urls import patterns, include, url

urlpatterns = patterns('callboard',
		url(r'^createadv/', 'views.createadv', name='createadv'),
		url(r'^advdetail/(?P<pk>\d+)/$', 'views.advdetail', name='advdetail'),
		url(r'^category/(?P<category>[0-9A-Za-z._%+-]+)/$', 'views.category', name='category'),
		url(r'^subcategory/(?P<subcategory>[0-9A-Za-z._%+-]+)/$', 'views.subcategory', name='subcategory'),
		url(r'^notes/', 'views.notes', name='notes'),

		)