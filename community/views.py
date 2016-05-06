
from django.db.models import F

from django.db.models import Max
from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django_comments.views.comments import post_comment
from avtocry.views import getuw
from community.models import Articles,Forums


# Create your views here.
@csrf_protect
def getArticle(request, article_id):

    args = {}
    args['username'] = request.user.username
    args['uw'] = getuw(args.get('username'))

    article = get_object_or_404(Articles,id=article_id)

    if request.user.username:
        args['email'] = request.user.email

    test = request.session.get('article_has_viewd_%s' % article_id,False)
    if request.session.get('article_has_viewd_%s' % article_id)!=True:
            request.session['article_has_viewd_%s' % article_id] = True
            article.views = article.views+1
            article.save()

    args['article']=article
    return render_to_response('article.html',
                              args,context_instance=RequestContext(request))


def getForum(request,forum_name):
    return HttpResponse('forums -'+forum_name)


def forums(request):
    args = {}
    args['username'] = request.user.username
    args['uw'] = getuw(args.get('username'))
    args['forums'] = Forums.objects.all()





    Articles.objects.annotate(max_date=Max('creation_date')).filter(creation_date=F('max_date'))
    return render_to_response('forums.html',
                              args,context_instance=RequestContext(request))