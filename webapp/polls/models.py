from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField("Pergunta", max_length=200)
    pub_date = models.DateTimeField("Data de publicação")

    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'


class Choice(models.Model):
    # chave estrangeira que vincula cada alternativa a uma pergunta
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200) # texto da alternativa
    votes = models.IntegerField(default=0) # contagem de votos na alternativa

    def __str__(self):
        return self.choice_text
