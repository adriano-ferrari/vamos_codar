# Generated by Django 5.0.1 on 2024-01-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='imagem',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images/user'),
        ),
    ]