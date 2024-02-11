from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# Define uma 'function view' chamada index
def index(request):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    return render(request, 'index.html', {'titulo': 'Enquetes'})

# Define uma 'function view' chamada ola
def ola(request):
    return HttpResponse('Olá Django')
