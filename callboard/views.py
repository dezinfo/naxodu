#-*- coding: utf-8 -*-
import django_filters
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet
from django_filters import FilterSet

from django.core.paginator import Paginator
from callboard.models import Category, Goods, SubCategory
from callboard.forms import AdverForm, GoodsImageGallery, ProductFilterForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from sxodu.views import getuw
from .forms import GoodsSearchForm
from .forms import AddAttrForm

import simplejson as json



from django.contrib import  auth

# Create your views here.


def advdetail(request,pk):
    # uw=getuw(request.user.username)
    args = {}
    # args['username'] = request.user.username
    # args['uw'] = uw
    test = request.session.get('has_viewd_%s' % pk,False)
    if request.session.get('has_viewd_%s' % pk)!=True:
            request.session['has_viewd_%s' % pk] = True
            # good = Goods.objects.get(pk=pk)
            good = get_object_or_404(Goods,pk=pk)
            good.views = good.views+1
            good.save()
            args['adv'] = good
            args['fotolist'] = good.goodsimagegallery_set.all().select_related('good')
                # GoodsImageGallery.objects.filter(good=pk)

            return  render_to_response('advdetail.html', args,context_instance=RequestContext(request))
    good = get_object_or_404(Goods,pk=pk)
    im = good.goodsimagegallery_set.all()

    args['adv'] = good
    args['fotolist'] = good.goodsimagegallery_set.all().select_related('good')
    return  render_to_response('advdetail.html', args,context_instance=RequestContext(request))




@login_required
def editadvert(request,adv_id):

    obj = get_object_or_404(Goods,pk=adv_id)

    if request.user.username == str(obj.user):

        # uw=getuw(request.user.username)
        args={}
        args['username'] = request.user.username
        # args['uw'] = uw
        args['object'] = obj

        return  render(request,'editadvert.html', args,context_instance=RequestContext(request))

    else:

        return HttpResponseRedirect('/')

@login_required
def createadv(request):


    # uw=getuw(request.user.username)


    url = request.POST.get('next','/')
    form = AdverForm(request.POST or None, request.FILES or None)

    if request.method =='POST':

     if form.is_valid():
         form.instance.user = request.user
         form.save()
         return redirect(url,{'username':request.user.username})

    args = {}
    # args.update(csrf(request))
    args['username'] = request.user.username
    args['form'] = form
    # args['uw'] = uw
    args['next'] = url



    return  render(request,'createadv.html', args,context_instance=RequestContext(request))

def notes(request):
    form = GoodsSearchForm(request.GET)
    test = request.GET.get('q')
    notes = form.search().models(Goods).filter(content=test).order_by('-text')

    return render_to_response('notes.html', {'notes': notes})


def autocomplete(request):
    sqs = SearchQuerySet().models(Goods).autocomplete(auto_name=request.GET.get('q', ''))

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





class ProductFilter(FilterSet):
    category = django_filters.CharFilter(name='category__id',distinct=True)
    subcategory = django_filters.CharFilter(name='subcategory__id',distinct=True)
    name = django_filters.CharFilter(name='name', lookup_type='icontains',distinct=True)
    min_price = django_filters.NumberFilter(name='price', lookup_type='gte',distinct=True)
    max_price = django_filters.NumberFilter(name='price', lookup_type='lte',distinct=True)
    moto_marka = django_filters.CharFilter(name='attributemap__attribute_value__vallue',lookup_type='icontains',distinct=True)
    moto_model = django_filters.CharFilter(name='attributemap__attribute_value__vallue',lookup_type='icontains',distinct=True)

    class Meta:
        model = Goods
        fields = [
            'min_price',
            'max_price',
            'category',
            'subcategory',
            'name',
            'description',
            'moto_marka',
            'moto_model'

        ]


def product_list(request):
    qs = Goods.objects.all().order_by('-update_date')
    sort = request.GET.get("sort")

    if sort:

        if sort == 'price':
            qs = sorted(Goods.objects.all(), key=lambda a: a.ua_price[0])
        else:
            qs = Goods.objects.all().order_by(sort)

    f = ProductFilter(request.GET, queryset=qs)
    return render(request,'callboard/goods_list.html',{"object_list":f})

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

            # if sort == 'price':
            #     qs = sorted(qs, key=lambda a: a.ua_price[0])
            # else:
            #     qs = qs.order_by(sort)


            qs = qs.order_by(sort)

        filter_class = self.filter_class

        if filter_class:
            f = filter_class(self.request.GET, queryset = qs)
            context["object_list"] = f
        return  context

class ProductListView(FilterMixin,ListView):
    model = Goods
    queryset = Goods.objects.only_active().select_related('user').order_by('-update_date')




    filter_class = ProductFilter

    def get_context_data(self,*args, **kwargs):
        username = auth.get_user(self.request).username
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        context['username'] = username
        context['cat_list'] = Category.objects.all()
        context['callboard'] = True

        if self.kwargs.get('category', None) != None:
         # context['subcat_list'] = SubCategory.objects.filter(category__slug=self.kwargs['category'])
         context['category'] = Category.objects.get(slug=self.kwargs['category'])


        if self.kwargs.get('subcategory', None) != None:
         # context['subcat_list'] = SubCategory.objects.filter(category__slug=self.kwargs['category'])
             subcategory = SubCategory.objects.get(slug=self.kwargs['subcategory'])

             print(self.kwargs)
             print(self.args)






             attr_form = AddAttrForm(self.request.POST or None, sub_category=subcategory)
             context['attr_form'] = attr_form

             context['subcategory'] = subcategory



        context['subcat_list'] = SubCategory.objects.all()
        context['query'] = self.request.GET.get('q')
        context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
        return context


    def get_queryset(self,*args,**kwargs):



        print(self.kwargs.get('category', None))
        print(self.kwargs.get('subcategory', None))





        if self.kwargs.get('category', None) != None:

            if self.kwargs.get('subcategory', None)!= None:
                qs = super(ProductListView,self).get_queryset(*args,**kwargs).\
                    filter(Q(category__slug=self.kwargs['category'])\
                           & Q(subcategory__slug=self.kwargs['subcategory']))
            else:
                qs = super(ProductListView,self).get_queryset(*args,**kwargs).filter(category__slug=self.kwargs['category'])
        else:
            qs = super(ProductListView,self).get_queryset(*args,**kwargs)


        # qs = super(ProductListView,self).get_queryset(*args,**kwargs)

        query = self.request.GET.get('q')

        if query:
            qs = SearchQuerySet().models(Goods).filter(text=query)
        return  qs

        # if query:
        #     qs = self.model.objects.filter(
        #         Q(name__icontains=query) |
        #         Q(description__in=query)
        #     )
        #     try:
        #         qs2 = self.model.objects.filter(
        #             Q(price=query)
        #         )
        #         qs = (qs|qs2).distinct()
        #     except:
        #         pass
        # return qs


def get_subcategory(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = category.subcategory_set.all()
    subcategories_dict = {}
    for subcategory in subcategories:
    # if your subcategory has field name
        subcategories_dict[subcategory.id] = subcategory.name

                                             # +' ['+str(subcategory.count_products())+']'

    return HttpResponse(json.dumps(subcategories_dict), content_type="application/json")


def get_attribute_form(request,subcategory_id):
    subcategory = SubCategory.objects.get(pk=subcategory_id)

    form = AddAttrForm(request.POST or None, sub_category=subcategory)


    return HttpResponse(form)





# def callboard (request):
#     sort = request.GET.get('sort')
#     args = {}
#     if sort:
#         args['sort'] = sort
#
#     return render_to_response('callboard/goods_list.html', args, context_instance=RequestContext(request))