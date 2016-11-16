import django_filters
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import simplejson as json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.exceptions import ImproperlyConfigured
# Create your views here.
from django.template.context_processors import request, csrf

from django.utils import timezone
from django.views.generic import ListView
from django_filters import FilterSet
from haystack.query import SearchQuerySet
from django.contrib import  auth

from auction.models import Auction
from auction.forms import AuctionFilterForm



def get_auction(request, auct_id):
    template = 'auct_detail.html'
    a = get_object_or_404(Auction, pk=auct_id)
    args = {}
    if a.is_canceled != True:

        args['object'] = a
        args['request'] = request
        args.update(csrf(request))

        return render_to_response('auct_detail.html',args)
    else:

        args['request'] = request

        return redirect('auction_list')



class AuctionFilter(FilterSet):
    category = django_filters.CharFilter(name='product__category',distinct=True)
    subcategory = django_filters.CharFilter(name='product__subcategory',distinct=True)
    name = django_filters.CharFilter(name='product__name', lookup_type='icontains',distinct=True)
    # min_price = django_filters.NumberFilter(name='min_price', lookup_type='gte',distinct=True)
    # max_price = django_filters.NumberFilter(name='max_price', lookup_type='lte',distinct=True)

    class Meta:
        model = Auction
        fields = [

            'category',
            'subcategory',
            'name'
        ]


class FilterMixin(object):
    filter_class = None

    search_ordering_param = "sort"

    def get_queryset(self,*args,**kwargs):
        try:
            qs = super(FilterMixin, self).get_queryset(*args,**kwargs)
            return qs
        except:
            raise ImproperlyConfigured("You must have a queryset to use the FilterMixin")


    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin,self).get_context_data(*args,**kwargs)
        qs = self.get_queryset()
        sort = self.request.GET.get(self.search_ordering_param)

        if sort:
            qs = qs.order_by(sort)

        filter_class = self.filter_class

        if filter_class:
            f = filter_class(self.request.GET, queryset = qs)
            context["object_list"] = f
        return  context



class AuctionListView(FilterMixin,ListView):
    model = Auction
    queryset = Auction.objects.filter(end_date__gte = timezone.now()).select_related('product').order_by('-update_date')
    filter_class = AuctionFilter

    def get_context_data(self,*args, **kwargs):

        context = super(AuctionListView,self).get_context_data(*args,**kwargs)

        context['query'] = self.request.GET.get('q')
        context["filter_form"] = AuctionFilterForm(data=self.request.GET or None)
        return context


    def get_queryset(self,*args,**kwargs):
        qs = super(AuctionListView,self).get_queryset(*args,**kwargs)
        query = self.request.GET.get('q')

        # if query:
        #     qs = SearchQuerySet().models(Auction).filter(text=query)
        # return  qs

        if query:
            qs = self.model.objects.filter(
                Q(name__icontains=query)
            )

        return qs



#
# def get_aucton_list(request):
#     args={}
#
#     ol = Auction.objects.filter(end_date__gte = timezone.now())
#
#     args['object'] = ol
#
#     return render_to_response('auctions.html',args,context_instance=RequestContext(request))

@login_required
def giveendprice(request,auct_id,user_id):

    auct = get_object_or_404(Auction,pk=auct_id)
    user = get_object_or_404(User,id=user_id)
    args = {}
    args['request'] = request

    bet = auct.end_price - auct.start_price
    auct.winner_bet.get_or_create(auction=auct.pk,user = user, bet=bet)

    return redirect('get_aucton_list',args)

@login_required
def set_bet(request):


    if request.method == "POST" and request.is_ajax:
        args = {}
        if request.user.id == int(request.POST['user_id']):

            print(request.POST)
            bet = request.POST['bet']
            auct_id = request.POST['auct_id']

            auct = get_object_or_404(Auction,pk=auct_id)
            user = request.user
            auct.winner_bet.get_or_create(auction=auct.pk,user = user, bet=bet)
            auct.save()
            args['bet'] = bet
            args['min_bet'] = auct.current_price()+auct.min_price_step
            print(args)
            return JsonResponse(args)
        else:
            args['error'] = 'Параметр транзакции не соответствует пользователю запроса'
            return JsonResponse(args)
    else:

        return HttpResponse(2)