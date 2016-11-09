from django.conf.urls import patterns, include, url

from auction.views import AuctionListView

urlpatterns = patterns('auction',
		# url(r'^$', 'views.get_aucton_list', name='auction'),
		url(r'^$', AuctionListView.as_view(), name='auction'),

		url(r'giveprice/(?P<auct_id>[0-9]+)/(?P<user_id>[0-9]+)/', 'views.giveendprice', name='give_end_price'),
		)