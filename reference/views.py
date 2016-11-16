from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.



def reference(request):
    return HttpResponse('It\'s references')