#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from callboard.models import Category, Goods
from callboard.forms import AdverForm, GoodsImageGallery
# from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from avtocry.views import getuw
from .forms import GoodsSearchForm
from haystack.query import SearchQuerySet
from .models import Goods
import simplejson as json
from haystack.query import SearchQuerySet
import avtocry.settings
# Create your views here.


def advdetail(request,pk):
    uw=getuw(request.user.username)
    args = {}
    args['username'] = request.user.username
    args['uw'] = uw
    test = request.session.get('has_viewd_%s' % pk,False)
    if request.session.get('has_viewd_%s' % pk)!=True:
            request.session['has_viewd_%s' % pk] = True
            good = Goods.objects.get(pk=pk)
            good.views = good.views+1
            good.save()
            args['adv'] = get_object_or_404(Goods,pk=pk)
            return  render_to_response('advdetail.html', args,context_instance=RequestContext(request))

    args['adv'] = get_object_or_404(Goods,pk=pk)
    return  render_to_response('advdetail.html', args,context_instance=RequestContext(request))

@login_required
def createadv(request):


    uw=getuw(request.user.username)


    url = request.POST.get('next','/')
    form = AdverForm(request.POST or None, request.FILES or None)

    if request.method =='POST':

     if form.is_valid():
         form.instance.user = request.user
         form.save()
         return redirect(url,{'username':request.user.username,'uw':uw})

    args = {}
    # args.update(csrf(request))
    args['username'] = request.user.username
    args['form'] = form
    args['uw'] = uw
    args['next'] = url


    return  render(request,'createadv.html', args,context_instance=RequestContext(request))

def notes(request):
    form = GoodsSearchForm(request.GET)
    test = request.GET.get('q')
    notes = form.search().models(Goods).filter(content=test).order_by('-text')

    return render_to_response('notes.html', {'notes': notes})


def autocomplete(request):
    sqs = SearchQuerySet().models(Goods).autocomplete(auto_name=request.GET.get('q', ''))[:5]
    suggestions = [result.auto_name for result in sqs]
    content_type = [result.content_type for result in sqs]
    #Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    jdata = json.dumps({
        'results': suggestions, 'content_type':content_type
    })
    return HttpResponse(jdata, content_type='application/json')

def category(request,category):
    return HttpResponse(category)

def subcategory(request,subcategory):
    return HttpResponse(subcategory)
