from django.conf.urls import  include, url
from .views import UserProductListView

from marketplace import views

urlpatterns = (
		url(r'^products/$', views.pruduct_list, name='pruduct_list'),
		url(r'^change_product_status/(?P<product_id>\d+)$', views.change_product_status, name='change_product_status'),
		url(r'^delete_product/(?P<product_id>\d+)$', views.delete_product, name='delete_product'),

		url(r'^shop/(?P<user_name>\w+)/$', UserProductListView.as_view(), name='user_pruduct_list'),


			   )