from django.urls import path

from . import views


urlpatterns = [
    #  caminho que vai carregar a view com o formulário
    path('accounts/signup',
         views.AccountCreateView.as_view(),
         name="signup"),
    path('accounts/<int:pk>/edit',
         views.AccountUpdateView.as_view(),
         name="account_edit"),
    path('accounts/profile',
         views.AccountTemplateView.as_view(),
         name="account_detail"),
]
