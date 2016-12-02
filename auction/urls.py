from django.conf.urls import  include, url
from auction import views

from auction.views import AuctionListView

urlpatterns = (
		# url(r'^$', 'views.get_aucton_list', name='auction'),
		url(r'^$', AuctionListView.as_view(), name='auction_list'),

		url(r'get_auction/(?P<auct_id>[0-9]+)/', views.get_auction, name='auction'),
		url(r'set_bet/', views.set_bet, name='set_bet'),
		url(r'giveprice/(?P<auct_id>[0-9]+)/', views.giveendprice, name='give_end_price'),
			   )