from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def index(request):
    return render(request, 'rango/index.html')
