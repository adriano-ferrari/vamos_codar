from django import forms # importa a classe form do django

from .models import Question # importa Question de models.py


# cria o ModelForm
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question # vincula o model ao form
        fields = ('question_text', 'pub_date') # campos a exibir no formulário
