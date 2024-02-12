from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
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
    #return render(request, 'index.html', {'titulo': 'Últimas Enquetes'})

    questions = Question.objects.all()
    context = {'all_questions': questions, 'titulo': 'Últimas Enquetes'}
    return render(request, 'polls/questions.html', context)  # renderiza e passa o contexto

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

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Criando uma pergunta'

        return context


# view baseada em função
@login_required  # controle de acesso usando o decorador de função
def question_create(request):
    context = {}  # dados para o contexto do form
    # cria o objeto form
    form = QuestionForm(request.POST or None, request.FILES or None)
    context['form'] = form
    context = {'form_title': 'Criando uma pergunta'}  # dados para o contexto do form

    if request.method == "POST":  # processa se o método de requisição for POST
        if form.is_valid():  # verifica se o form é válido
            form.save()  # salva os dados do form no modelo
            messages.success(request, 'Pergunta criada com sucesso.')
            return redirect("index")  # redireciona em caso de sucesso

    return render(request, 'polls/question_form.html', context)  # carrega o form no template


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('index')
    form_class = QuestionForm  # compartilha o form criado anteriormente
    success_message = 'Pergunta atualizada com sucesso.'

    # implementa o método que conclui a ação com sucesso
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(QuestionUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a pergunta'

        return context


@login_required
def question_update(request, question_id):
    context = {}  # dados para o contexto do form
    # recupera a pergunta pelo id (chave primária)
    question = get_object_or_404(Question, id=question_id)
    # cria o objeto form já preenchido com os dados da pergunta
    form = QuestionForm(request.POST or None, instance=question)
    context['form'] = form
    context = {'form_title': 'Editando a pergunta'}  # dados para o contexto do form

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Pergunta atualizada com sucesso.')
            return redirect("index")

    return render(request, 'polls/question_form.html', context)
