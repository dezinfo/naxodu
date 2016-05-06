from django.conf.urls import patterns, include, url

urlpatterns = patterns('community',
		url(r'^article/(?P<article_id>\d+)/$', 'views.getArticle', name='article'),
		url(r'^forum/(?P<forum_name>[0-9A-Za-z._%+-]+)/$', 'views.getForum', name='forum'),
		url(r'^', 'views.forums', name='forums'),
		)