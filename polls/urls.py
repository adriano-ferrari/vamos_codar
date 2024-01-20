from django.urls import path

from polls.views import index, ola, QuestionCreateView, question_create

urlpatterns = [
    path('index/', index, name='index'),
    path('ola/', ola, name='ola'),
    path('enquete/add', QuestionCreateView.as_view(), name="poll_add"),
    path('pergunta/create', question_create, name="poll_create"),
]
