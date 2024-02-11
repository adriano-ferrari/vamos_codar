from django.urls import path

from . import views


urlpatterns = [
    #  caminho que vai carregar a view com o formulário
    path('accounts/signup', views.AccountCreateView.as_view(), name="signup"),
]
