from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from shop.models import Order
from callboard.models import Goods
from django.db.models import Q
from django.template import RequestContext


# Create your views here.

def order_list(request, user_name):
    if request.user.username == user_name:
        orders_to_me = Order.objects.filter(Q(seller__username=user_name) & ~Q(order_status = 'Draft'))
        my_orders = Order.objects.filter(Q(buyer__username=user_name))
        market = Goods.objects.filter(user__username=user_name)
        return render_to_response('orders.html', {'my_orders': my_orders,'orders_to_me':orders_to_me,'market':market},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
