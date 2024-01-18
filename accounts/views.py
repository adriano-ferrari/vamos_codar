# from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password # para criptografar a senha
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.forms import AccountSignupForm # importa o form de registro
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model() # obtém o model padrão para usuários do Django


class AccountCreateView(CreateView):
    model = User # conecta o model a view
    template_name = 'registration/signup_form.html' # template para o form HTML
    form_class = AccountSignupForm # conecta o form a view
    success_url = reverse_lazy('login') # destino após a criação do novo usuário
    success_message = 'Usuário criado com sucesso!'
    
    def form_valid(self, form) -> HttpResponse: # executa se os dados válidos
        form.instance.password = make_password(form.instance.password)
        form.save()
        messages.success(self.request, self.success_message)        
        return super(AccountCreateView, self).form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = ('first_name', 'email', 'imagem')
    success_url = reverse_lazy('index')
    success_message = 'Perfil atualizado com sucesso.'

    # editar o próprio perfil
    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = self.request.user
        if user is None or user.is_authenticated or user_id != user.id:
            return User.objects.none()
        return User.objects.filter(id=user_id)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(AccountUpdateView, self).form_valid(form)
