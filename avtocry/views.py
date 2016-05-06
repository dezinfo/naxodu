#-*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.shortcuts import render_to_response
from django.contrib import  auth
from django.template import RequestContext

from callboard.models import Goods
from community.models import Forums, Articles
from django_comments.models import Comment
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

    username = auth.get_user(request).username


    content = Goods.objects.filter().order_by('-creation_date')
    forums = Articles.objects.filter().order_by('-creation_date')[:10]

    args={}
    args['username'] = username
    args['uw'] = getuw(username)
    args['content'] =content
    args['forums'] =forums


    return render_to_response('index.html',args,context_instance=RequestContext(request))