from django.contrib import admin

from .models import Question # importa o model que vamos habilitar no admin site

# Register your models here.
@admin.register(Question) # registar o model Question e habilita
class QuestionAdmin(admin.ModelAdmin): # configura o model Question no admin site.
    list_display = ('id', 'question_text', 'pub_date') # campos para listar.
    list_filter = ('pub_date',) # campos que poderão ser filtrados.
