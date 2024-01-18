from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question


# Define uma view baseada em funcão.
def index(request):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    aviso = 'Aviso importante: esta página não exige login.'
    messages.warning(request, aviso)
    return render(request, 'index.html', {'titulo': 'Últimas Enquetes'})


# Define uma view baseada em funcão
@login_required # controle de acesso usando o decorador de função
def ola(request):
    # return HttpResponse('Olá Django!')
    questions = Question.objects.all()
    context = {'all_questions': questions}
    return render(request, 'polls/questions.html', context)
