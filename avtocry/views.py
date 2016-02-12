#-*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.shortcuts import render_to_response
from django.contrib import  auth

def index(request):

    username = auth.get_user(request).username

    uw = username[0].capitalize()

    return render_to_response('index.html',{'username':auth.get_user(request).username, 'uw':uw})