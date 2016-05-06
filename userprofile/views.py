from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse

# Create your views here.

@login_required
def inbox(request):
    return HttpResponse('test')
