from django.conf.urls import include, url
from reviews import views

urlpatterns = (
		url(r'^$', views.reviews, name='reviews'),


			   )