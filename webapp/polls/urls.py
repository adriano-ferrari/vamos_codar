from django.urls import path

# Na linha abaixo importamos as "functions views".
from .views import (
    index, ola,
    QuestionCreateView, question_create,
    QuestionUpdateView, question_update,
    QuestionDeleteView, question_delete,
    QuestionDetailView, QuestionListView,
    SobreTemplateView
)


urlpatterns = [
    path('index/', index, name='index'),  # cria a rota /index
    path('ola/', ola, name='ola'),  # cria a rota /ola

    path('enquete/add', QuestionCreateView.as_view(), name="poll_add"),
    path('pergunta/create', question_create, name="poll_create"),
    path('enquete/<int:pk>/edit', QuestionUpdateView.as_view(), name="question_edit"),
    path('pergunta/<int:question_id>/update', question_update, name="question_update"),
    path('enquete/<int:pk>/delete', QuestionDeleteView.as_view(), name="question_delete"),
    path('pergunta/<int:question_id>/remove', question_delete, name="question_remove"),
    path('enquete/<int:pk>/show', QuestionDetailView.as_view(), name="question_detail"),
    path('enquete/list', QuestionListView.as_view(), name="polls_list"),
    path('about-us', SobreTemplateView.as_view(), name="about_page"),
]
