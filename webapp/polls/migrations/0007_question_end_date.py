# Generated by Django 5.0.1 on 2024-02-17 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_question_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de encerramento'),
        ),
    ]
