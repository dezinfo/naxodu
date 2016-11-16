from django.conf.urls import include, url

from reference import views

urlpatterns = (
					   url(r'^$', views.reference, name='reference'),


			   )