from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404, render_to_response
from userprofile.models import UserProfileTable

# Create your views here.

@login_required
def inbox(request):
    return HttpResponse('test')



@login_required
def myprofile(request):
    args = {}
    p = get_object_or_404(UserProfileTable,username = request.user)
    args['objects'] = p
    return render(request,'myprofile.html',args)


@login_required
def userprofile(request,username):
    args = {}
    p = get_object_or_404(UserProfileTable,username__username = username)
    args['objects'] = p

    return render(request,'userprofile.html',args)




