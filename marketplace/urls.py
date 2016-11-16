from django.conf.urls import  include, url
from .views import UserProductListView

from marketplace import views

urlpatterns = (
		url(r'^(?P<user_name>\w+)/products/$', views.pruduct_list, name='pruduct_list'),
		url(r'^shop/(?P<user_name>\w+)/$', UserProductListView.as_view(), name='user_pruduct_list'),


			   )