from django.conf.urls import patterns, include, url
from .views import UserProductListView
urlpatterns = patterns('marketplace',
		url(r'^(?P<user_name>\w+)/products/$', 'views.pruduct_list', name='pruduct_list'),
		url(r'^shop/(?P<user_name>\w+)/$', UserProductListView.as_view(), name='user_pruduct_list'),


		)