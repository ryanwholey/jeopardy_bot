import json
import datetime
from django.utils import timezone

from django.core.management.base import BaseCommand

from jeopardy.models import Question

class Command(BaseCommand):

    def handle(slef, *args, **kwargs):
        with open('/Users/rwholey/bots/trabek_bot/JEOPARDY_QUESTIONS1.json') as json_file:
            json_data = json.load(json_file)
            for obj in json_data:
                date = datetime.datetime.strptime(obj.get('air_date'), '%Y-%m-%d')
                my_datetime = timezone.make_aware(date, timezone.get_current_timezone())
                try:
                    val = int((obj.get('value')[1:]).replace(',',''))
                except:
                    val = 200
                shw = int(obj.get('show_number'))

                Question.objects.get_or_create(category=obj.get('category'), air_date=my_datetime, question=obj.get('question'), value=val, answer=obj.get('answer'), jeopardy_round=obj.get('round'), show=shw, )

