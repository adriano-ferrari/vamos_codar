from django.urls import path

# Na linha abaixo importamos as "functions views".
from .views import index, ola, QuestionCreateView, question_create


urlpatterns = [
    path('index/', index, name='index'),  # cria a rota /index
    path('ola/', ola, name='ola'),  # cria a rota /ola

    path('enquete/add', QuestionCreateView.as_view(), name="poll_add"),
    path('pergunta/create', question_create, name="poll_create"),
]
