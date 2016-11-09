from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404, render_to_response
from userprofile.models import UserProfileTable

# Create your views here.

@login_required
def inbox(request):
    return HttpResponse('test')


@login_required
def profile(request,username):
    args = {}
    if username == request.user.username:

        p = get_object_or_404(UserProfileTable,username = request.user.id)
        args['objects'] = p

        return render_to_response('userprofile.html',args)

    return HttpResponse('/')


def userprofile(request, username):
     return HttpResponse('Профиль пользователя:'+ username)
