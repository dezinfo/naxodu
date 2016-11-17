from django.db.models import F
from django.db.models import Max
from django.shortcuts import render,redirect, render_to_response, get_object_or_404, HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from community.models import Articles,Forums
from community.forms import NewArticleForm, CreateForum
from django.contrib.auth.decorators import login_required



@login_required
def createforum (request):
     args={}
     form = CreateForum(request.POST, request.FILES)
     url = request.POST.get('next','/')
     args['form'] = CreateForum(request.POST, request.FILES)
     args['request'] = request
     if request.method == 'POST':
        if form.is_valid():
            form.instance.username = request.user
            form.instance.official_status = False
            form.save()

            return redirect(url, {'username': request.user.username}, args)


     return  render(request,'createforum.html', args)

@login_required
def newArticle(request,forum_id):

    args={}

    args['forum_id'] = forum_id
    args['request'] = request
    forum =get_object_or_404(Forums,slug=forum_id)

    if (forum==forum_id) is not None:
        # uw = getuw(request.user.username)
        form = NewArticleForm(request.POST)
        url = request.POST.get('next','/')
        if request.method == 'POST':


            if form.is_valid():
                form.instance.username = request.user
                form.instance.forum_id = forum.pk
                form.save()
                return redirect(url, {'username': request.user.username})



        args['username'] = request.user.username
        # args['uw'] = uw
        args['form'] = form
        args['next'] = url
        args['request'] = request

        return  render(request,'newarticle.html', args)

    else:

        return HttpResponseRedirect('/')


# Create your views here.
@csrf_protect
def getArticle(request, article_id):

    args = {}
    args['username'] = request.user.username
    # args['uw'] = getuw(args.get('username'))

    article = get_object_or_404(Articles,id=article_id)

    if request.user.username:
        args['email'] = request.user.email

    test = request.session.get('article_has_viewd_%s' % article_id,False)

    if (request.session.get('article_has_viewd_%s' % (article_id))!=True or request.session.get('article_has_viewd_%s' % (request.user.username))!=True):
            request.session['article_has_viewd_%s' % (article_id)] = True
            request.session['article_has_viewd_%s' % (request.user.username)] = True
            article.views = article.views+1
            article.save()

    args['article']=article
    args['request'] = request
    return render(request,'article.html',args)


def getForum(request,forum_name):





    forum = get_object_or_404(Forums, slug=forum_name)
    forum_list = Articles.objects.filter(forum=forum)
    args={}
    args['username'] = request.user.username
    # args['uw'] = getuw(request.user.username)
    args['forum_id'] = forum_name
    args['forum_list'] = forum_list
    args['forum'] = forum
    args['request'] = request
    return render(request,'forum.html',args)


def forums(request):
    args = {}
    args['username'] = request.user.username
    args['request'] = request
    # args['uw'] = getuw(args.get('username'))
    args['off_forums'] = Forums.objects.filter(official_status=True)
    args['user_forums'] = Forums.objects.filter(official_status=False)
    args['forums'] = Articles.objects.filter().order_by('-creation_date')[:10]



    Articles.objects.annotate(max_date=Max('creation_date')).filter(creation_date=F('max_date'))

    return render(request,'forums.html',
                              args)