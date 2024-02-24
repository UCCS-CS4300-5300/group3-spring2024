from django.db.models import indexes
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
import json

'''
General Views
'''
def home(request):
  return render(request, 'home.html')