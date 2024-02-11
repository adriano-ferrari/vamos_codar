from django.urls import path

# Na linha abaixo importamos as "functions views".
from .views import index, ola


urlpatterns = [
    path('index/', index, name='index'),  # cria a rota /index
    path('ola/', ola, name='ola'),  # cria a rota /ola
]
