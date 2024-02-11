from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Question  # Acrescentar


# Create your views here.

# Define uma 'function view' chamada index
def index(request):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    aviso = 'Aviso importante: esta página não exige login.'
    messages.warning(request, aviso)
    return render(request, 'index.html', {'titulo': 'Últimas Enquetes'})

# Define uma 'function view' chamada ola
@login_required  # controle de acesso usando o decorador de função
def ola(request):  # Modificar
    # return HttpResponse('Olá django')
    questions = Question.objects.all() # recupera todos questions do banco de dados
    context = {'all_questions': questions } # cria um dicionário com todas as perguntas
    return render(request, 'polls/questions.html', context) # renderiza o template e passa o contexto
