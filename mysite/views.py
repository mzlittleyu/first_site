# encoding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
def homepage(request):
    return render(request,'homepage/homepage.html')