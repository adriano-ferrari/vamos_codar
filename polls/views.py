from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Question


# Define uma view baseada em funcão.
def index(request):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    return render(request, 'index.html', {'titulo': 'Últimas Enquetes'})


# Define uma view baseada em funcão
@login_required
def ola(request):
    # return HttpResponse('Olá Django!')
    questions = Question.objects.all()
    context = {'all_questions': questions}
    return render(request, 'polls/questions.html', context)
