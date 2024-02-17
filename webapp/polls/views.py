import csv
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView, FormView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Question, Choice  # Acrescentar
from .forms import QuestionForm, QuestionImportForm  # importa a classe QuestionForm

User = get_user_model()

# Create your views here.

# Define uma 'function view' chamada index
def index(request, categoria=None):
    # return HttpResponse('Olá Django - index')
    # return render(request, 'index.html')
    aviso = 'Aviso importante: esta página não exige login.'
    messages.warning(request, aviso)
    #return render(request, 'index.html', {'titulo': 'Últimas Enquetes'})

    if categoria is not None:
        questions = Question.objects.filter(categoria=categoria)
    else:
        questions = Question.objects.all()

    categorias = Question.objects.all().values_list(
        'categoria', flat=True
    ).exclude(
        categoria=None
    ).distinct()

    context = {
        'all_questions': questions,
        'titulo': 'Últimas Enquetes',
        'categoria': categoria,
        'all_categorias': categorias
        }
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
    fields = ('question_text', 'pub_date', 'categoria')  # campos que estarão disponíveis no form
    success_url = reverse_lazy('index')  # URL para redirecionado em caso de sucesso
    success_message = 'Pergunta criada com sucesso.'

    # implementa o método que conclui a ação com sucesso (dentro da classe)
    def form_valid(self, form):
        form.instance.author = self.request.user  # usuário logado
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


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete_form.html'
    success_url = reverse_lazy('index')
    success_message = 'A pergunta foi excluída com sucesso.'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(QuestionDeleteView, self).form_valid(form)


@login_required
def question_delete(request, question_id):
    context = {}
    # recupera a pergunta pelo id (chave primária)
    question = get_object_or_404(Question, id=question_id)
    context['object'] = question

    if request.method == "POST":
        # Exclui o objeto / registro.
        question.delete()
        messages.success(request, 'A pergunta foi excluída com sucesso.')
        return redirect("index")

    return render(request, "polls/question_confirm_delete_form.html", context)


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question = kwargs.get('object')
        context['total_votes'] = question.get_total_votes()

        return context


class QuestionListView(ListView):
    model = Question
    template_name = 'polls/question_list.html'
    context_object_name = 'questions'
    paginate_by = 5  # quantidade de itens por página
    ordering = ['-pub_date']  # ordenar pela data de publicaćão de forma inversa - decrescente


class SobreTemplateView(TemplateView):
    template_name = 'polls/sobre.html'


@login_required()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
            session_user = get_object_or_404(User, id=request.user.id)
            selected_choice.votes += 1
            selected_choice.save(user=session_user)

        except (KeyError, Choice.DoesNotExist):
            messages.error(request, 'Selecione uma alternativa para votar')

        except (ValidationError) as error:
            messages.error(request, error.message)

        else:
            messages.success(request, 'O seu voto foi registrado com sucesso.')
            return redirect(reverse_lazy('poll_results', args=(question.id,)))

    context = {'question': question}
    return render(request, 'polls/question_detail.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    context['votes'] = question.get_results()

    return render(request, 'polls/results.html', context)


class ChoiceCreateView(LoginRequiredMixin, CreateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text',)
    success_message = 'Alternativa criada com sucesso!'

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        return super(ChoiceCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChoiceCreateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Alternativa para: {self.question.question_text}'
        return context

    def form_valid(self, form):
        try:
            form.instance.question = self.question
            response = super(ChoiceCreateView, self).form_valid(form)
        except (ValidationError) as error:
            messages.error(self.request, error.message)
            return self.form_invalid(form)
        else:
            messages.success(self.request, self.success_message)
            return response

    def get_success_url(self, *args, **kwargs):
        question_id = self.kwargs.get('pk')
        return reverse_lazy('question_edit', kwargs={'pk': question_id})


class ChoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text',)
    success_message = 'Alternativa atualizada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super(ChoiceUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a alternativa'
        
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(ChoiceUpdateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})


class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Choice
    template_name = 'polls/choice_confirm_delete_form.html'
    success_message = 'Alternativa excluída com sucesso!'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(ChoiceDeleteView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})


class QuestionImportView(LoginRequiredMixin, FormView):
    template_name = 'polls/question_import_form.html'
    parent_class = FormView
    form_class = QuestionImportForm
    success_url = reverse_lazy('index')
    error_message = 'Ocorreu algum erro inesperado.'

    def form_valid(self, form):
        if self.request.method == 'POST':

            tmp_file_name = form.cleaned_data.get('tmp_file_name')

            csv_file = open(tmp_file_name)
            csv_reader = csv.DictReader(csv_file)
            question_count = 0

            # question_text,pub_date,2023-10-22
            for row in csv_reader:
                pub_date = datetime.fromisoformat(row['pub_date'])
                question = Question(
                    question_text=row['question_text'],
                    pub_date=pub_date
                )
                question.save()
                question_count += 1

            success_message = f'{question_count} Perguntas importadas com sucesso.'
            messages.success(self.request, success_message)

        return super(QuestionImportView, self).form_valid(form)


def poll_send(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question_url = reverse_lazy('question_detail', args=[question_id])
    try:
        email = request.POST.get('email')
        if len(email) < 5:
            raise ValueError('E-mail inválido')

        link = f'{request._current_scheme_host}{question_url}'
        template = 'polls/question_send'
        text_message = render_to_string(f'{template}.txt', {'question_link': link})
        html_message = render_to_string(f'{template}.html', {'question_link': link})
        send_mail(
            subject='Encontrei esta enquete e acredito que pode te interessar!',
            message=text_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message,
        )
        messages.success(
            request, 'Enquete compartilhada com sucesso.'
        )
    except ValueError as error:
        messages.error(request, error)
    except Exception as error:
        messages.error(request, 'Erro ao enviar mensagem!')

    return redirect(question_url)


@login_required
def question_export(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment: filename="questions.csv"'},
    )

    questions = Question.objects.all()

    writer = csv.writer(response)
    writer.writerow(['question_text', 'pub_date'])

    for q in questions:
        writer.writerow([q.question_text, f'{q.pub_date:%Y-%m-%d}'])

    return response
