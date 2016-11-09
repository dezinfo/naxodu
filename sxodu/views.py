#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

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




    content = Goods.objects.only_active().order_by('-creation_date')[:6]

    aukc = None


    forums = Articles.objects.all().order_by('-creation_date')[:5]

    args={}
    # args['username'] = username
    # args['uw'] = getuw(username)
    args['content'] =content
    args['forums'] =forums




    return render_to_response('index.html',args,context_instance=RequestContext(request))