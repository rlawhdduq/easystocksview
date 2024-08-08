from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello1351351 Python, You\'re at the stocks index.')
