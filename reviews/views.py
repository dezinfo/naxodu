from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def reviews(request):
     return HttpResponse('It\'s reviews')