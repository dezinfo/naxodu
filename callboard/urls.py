from django.conf.urls import include, url
from .views import ProductListView
from callboard import views


urlpatterns = (
		url(r'^createadv/', views.createadv, name='createadv'),
		url(r'^editadvert/(?P<adv_id>\d+)/$', views.editadvert, name='editadvert'),
		url(r'^advdetail/(?P<pk>\d+)/', views.advdetail, name='advdetail'),

		url(r'^notes/', views.notes, name='notes'),
		url(r'^$',ProductListView.as_view() , name='callboard'),
		# url(r'^$','views.product_list' , name='callboard'),
		url(r'^get_subcategory/(?P<category_id>[0-9]+)/$', views.get_subcategory, name='get_subcategory'),
		url(r'^get_subcategory_list/(?P<category_id>[0-9]+)/$', views.get_subcategory_list, name='get_subcategory_list'),
		url(r'^get_attribute_form/(?P<subcategory_id>[0-9]+)(?:/(?P<it_creation>[a-zA-Z]+))?', views.get_attribute_form, name='get_attribute_form'),
		url(r'^(?P<category>[0-9A-Za-z._%+-]+)/$', ProductListView.as_view(), name='category'),
		url(r'^(?P<category>[0-9A-Za-z._%+-]+)/(?P<subcategory>[0-9A-Za-z._%+-]+)/$', ProductListView.as_view(), name='subcategory'),
		url(r'^(?P<user>[0-9A-Za-z._%+-]+)/?(P<category>[0-9A-Za-z._%+-]+)/(?P<subcategory>[0-9A-Za-z._%+-]+)/$', ProductListView.as_view(), name='subcategory'),



			   )


