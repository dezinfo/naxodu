#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from naxodu import settings
from callboard.models import Goods
from community.models import Forums, Articles
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True



def getuw(username):

      if username:
        uw = username[0].capitalize()

      else:
        uw = None

      return  uw

def index(request):


    if settings.UNDER_CUNSTRUCTION:
        return render(request,'index1.html')

    content = Goods.objects.only_active().order_by('-order_date')[:6]

    aukc = None


    forums = Articles.objects.all().order_by('-creation_date')[:5]

    args={}
    # args['username'] = username
    # args['uw'] = getuw(username)
    args['content'] =content
    args['forums'] =forums
    # args['request'] = request


    # context.Context




    return render(request,'index.html',context=args)