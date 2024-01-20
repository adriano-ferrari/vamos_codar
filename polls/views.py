from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Question
from polls.forms import QuestionForm


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


# view baseada em classe (genérica)
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ('question_text', 'pub_date')
    success_url = reverse_lazy('index')
    success_message = 'Pergunta criada com sucesso.'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(QuestionCreateView, self).form_valid(form)


# view baseada em função
@login_required
def question_create(request):
    context = {} # dados para o contexto do form
    # cria o objeto form
    form = QuestionForm(request.POST or None, request.FILES or None)
    context['form'] = form

    if request.method == 'POST': # processa se o método de requisição for POST
        if form.is_valid(): # verifica se o form é válido
            form.save() # salva os dados do form no modelo
            messages.success(request, 'Pergunta criada com sucesso.')
            return redirect('index') # redireciona em caso de sucesso

    return render(request, 'polls/question_form.html', context) # carrega o form no template
