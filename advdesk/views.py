#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from advdesk.models import Category, Goods
from advdesk.forms import AdverForm
from django.core.context_processors import csrf




# Create your views here.

def createadv(request):



    if request.method =='POST':
     form = AdverForm(request.POST)
     if form.is_valid():
         form.save()

     return HttpResponseRedirect('/')

    args = {}
    args.update(csrf(request))
    args['form'] = AdverForm()

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        form.save()
        return redirect('/', {'zip': Goods.objects.all(), 'username':self.request.user})


    return  render_to_response('createadv.html', args)