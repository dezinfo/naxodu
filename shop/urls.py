from django.conf.urls import patterns, include, url

urlpatterns = patterns('shop',
		url(r'^orders/(?P<user_name>\w+)/$', 'views.order_list', name='orders'),


		)