"""avtocry URL Configuration 556777777

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.utils import duration
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    url(r'^secret/', include(admin.site.urls)),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', 'avtocry.views.index'),
    url(r'^callboard/', include('callboard.urls')),
    url(r'^community/', include('community.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^reviews/', include('reviews.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^userprofile/', include('userprofile.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^autocomplete/', 'callboard.views.autocomplete', name='autocomplete'),
    url(r'^tinymce/', include('tinymce.urls')),


]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)