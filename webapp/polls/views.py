from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Question  # Acrescentar
from .forms import QuestionForm  # importa a classe QuestionForm


# Create your views here.

# Define uma 'function view' chamada index
def index(request):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    aviso = 'Aviso importante: esta página não exige login.'
    messages.warning(request, aviso)
    return render(request, 'index.html', {'titulo': 'Últimas Enquetes'})

# Define uma 'function view' chamada ola
def ola(request):  # Modificar
    # return HttpResponse('Olá django')
    questions = Question.objects.all()  # recupera todos questions do banco de dados
    context = {'all_questions': questions}  # cria um dicionário com todas as perguntas
    return render(request, 'polls/questions.html', context)  # renderiza o template e passa o contexto


# view baseada em classe (genérica)
class QuestionCreateView(LoginRequiredMixin, CreateView):  # view baseada em classe, usa herança
    model = Question  # vincula o model a view para gerar o form HTML
    template_name = 'polls/question_form.html'  # template que monta o form
    fields = ('question_text', 'pub_date', )  # campos que estarão disponíveis no form
    success_url = reverse_lazy('index')  # URL para redirecionado em caso de sucesso
    success_message = 'Pergunta criada com sucesso.'

    # implementa o método que conclui a ação com sucesso (dentro da classe)
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(QuestionCreateView, self).form_valid(form)


# view baseada em função
@login_required  # controle de acesso usando o decorador de função
def question_create(request):
    context = {}  # dados para o contexto do form
    # cria o objeto form
    form = QuestionForm(request.POST or None, request.FILES or None)
    context['form'] = form

    if request.method == "POST":  # processa se o método de requisição for POST
        if form.is_valid():  # verifica se o form é válido
            form.save()  # salva os dados do form no modelo
            messages.success(request, 'Pergunta criada com sucesso.')
            return redirect("index")  # redireciona em caso de sucesso

    return render(request, 'polls/question_form.html', context)  # carrega o form no template
