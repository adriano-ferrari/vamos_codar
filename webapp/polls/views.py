from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import Question  # Acrescentar

# Define uma 'function view' chamada index
def index(request):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    return render(request, 'index.html', {'titulo': 'Enquetes'})

# Define uma 'function view' chamada ola
def ola(request):  # Modificar
    # return HttpResponse('Olá django')
    questions = Question.objects.all() # recupera todos questions do banco de dados
    context = {'all_questions': questions } # cria um dicionário com todas as perguntas
    return render(request, 'polls/questions.html', context) # renderiza o template e passa o contexto