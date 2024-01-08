from django.shortcuts import render
from django.http import HttpResponse


# Define uma view baseada em funcão.
def index(request):
    # return HttpResponse('Olá Django - index')
    return render(request, 'index.html')


# define uma view baseada em funcão
def ola(request):
    return HttpResponse('Olá Django!')
