from django import forms  # importa a classe form do django
from django.core.files.temp import NamedTemporaryFile

from .models import Question  # importa Question de models.py


# cria o ModelForm
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # vincula o model ao form
        fields = ('question_text', 'pub_date', 'categoria', 'end_date')  # campos a exibir no formulário
        widgets = {
            'pub_date': forms.widgets.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'end_date': forms.widgets.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'type': 'datetime-local'}
            )
        }


class QuestionImportForm(forms.Form):
    import_file = forms.FileField(label='Arquivo para Importacao')

    def clean(self):
        cleaned_data = super().clean()
        import_data = cleaned_data.get('import_file')

        if not self.has_error('import_file'):

            # Cria um arquivo temporário
            csv_temp_file = NamedTemporaryFile(delete=False)

            # Salva o arquivo no disco
            with csv_temp_file as uploaded_file:
                for chunk in import_data.chunks():
                    uploaded_file.write(chunk)

            cleaned_data['tmp_file_name'] = csv_temp_file.name

        return cleaned_data
