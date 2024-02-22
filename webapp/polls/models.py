from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Question(models.Model):
    question_text = models.CharField("Pergunta", max_length=200)
    pub_date = models.DateTimeField("Data de publicação")
    author = models.ForeignKey(
        User,  # chave estrangeira vinculada ao usuário
        editable=False,  # não permite alteracao
        null=True,  # permite valor nulo para não conflitar com registros existentes
        on_delete=models.DO_NOTHING  # não faz n ada ao excluir o usuário autor
    )
    categoria = models.CharField(
        'Categoria',
        max_length=15,
        choices=[
            ('geral', 'Geral'),
            ('preferências', 'Preferências'),
            ('política', 'Política')
        ],
        default=None,
        null=True
    )
    end_date = models.DateTimeField('Data de encerramento', null=True, blank=True)

    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'

    def __str__(self):
        return self.question_text

    def get_total_votes(self):
        votes = Choice.objects.filter(question=self).aggregate(
            total=models.Sum('votes')
        )
        return votes.get('total')

    def get_results(self):
        total_votes = self.get_total_votes()
        votes = []
        for choice in self.choice_set.all():
            percentage = 0
            if choice.votes > 0 and total_votes > 0:
                percentage = choice.votes / total_votes * 100

            votes.append(
                {
                    'text': choice.choice_text,
                    'votes': choice.votes,
                    'percentage': round(percentage, 2)
                }
            )

        return votes


class Choice(models.Model):
    # chave estrangeira que vincula cada alternativa a uma pergunta
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)  # texto da alternativa
    votes = models.IntegerField(default=0)  # contagem de votos na alternativa

    def __str__(self):
        return self.choice_text
    
    def save(self, user=None, *args, **kwargs):
        if self.id is None:
            choices_count = Choice.objects.filter(question=self.question).count()
            max_choices = settings.MAX_CHOICES_PER_QUESTION
            if choices_count == max_choices:
                raise ValidationError(f'Não é permitido adicionar mais de {max_choices} alternativas')

        # Salvando um voto
        if self.id is not None and user is not None:
            end_date = self.question.end_date
            if end_date is not None and end_date < timezone.now():
                raise ValidationError('Não é permitido votar em uma pergunta encerrada.')

            question_user = QuestionUser.objects.filter(
                user=user,
                question=self.question
            ).count()
            if question_user > 0:
                raise ValidationError('Não é permitido votar mais de uma vez')
        
            question_user = QuestionUser.objects.create(
                user=user,
                question=self.question
            )

            question_user.save()
        
        super().save(*args, **kwargs)


class QuestionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
