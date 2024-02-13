# Python
import csv
from datetime import datetime

# Django
from django.core.management.base import BaseCommand
from django.conf import settings

# 3rdApps

# App
from webapp.polls.models import Question


class Command(BaseCommand):
    help = 'Data import'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Arquivo CSV')

    def handle(self, *args, **kwargs):
        csv_file = open(f'{settings.BASE_DIR}/{kwargs["csv_file"]}')
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            print(row)
            pub_date = datetime.fromisoformat(row['pub_date'])
            question = Question(
                question_text=row['question_text'],
                pub_date=pub_date
            )
            question.save()
