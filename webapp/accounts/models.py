from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):  # herda o model User base padrão do Django
    data_nascimento = models.DateField(
        "Data de Nascimento",
        null=True,
        blank=True
    )
    cpf = models.CharField(
        "CPF",
        max_length=11,
        null=True,
        blank=True
    )
    imagem = models.FileField(
        upload_to='images/user',
        default=None,
        null=True,
        blank=True  # permite apagar o arquivo
    )
