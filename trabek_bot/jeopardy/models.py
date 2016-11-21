from django.db import models
import datetime


class Question(models.Model):
    category = models.CharField(db_index=True, blank=False, max_length=255)
    air_date = models.DateTimeField(null=True, blank=True)
    question = models.TextField(blank=False)
    value = models.IntegerField(blank=False)
    answer = models.CharField(blank=False, max_length=255)
    jeopardy_round = models.CharField(blank=True, max_length=255)
    show = models.IntegerField(null=True, blank=True)

    @classmethod
    def create(cls, category, air_date, question, value, answer, jeopardy_round, show):
        date = datetime.datetime.strptime(air_date, '%Y-%m-%d')
        try:
            val_string = value[1:]
            val = int(val_string)
        except:
            print value
            val = 200

        q = cls(
            category=category,
            air_date=date,
            question=question,
            value=val,
            answer=answer,
            jeopardy_round=jeopardy_round,
            show=int(show),
        )
        return q

class Player(models.Model):
    name = models.CharField(
            db_index=True,
            max_length=255,
            blank=False,
            unique=True,
        )
    score = models.IntegerField(
            default=0,
        )
    asked = models.IntegerField(
            default=0,
        )
    right_questions = models.ManyToManyField(
            Question,
            blank=True,
            related_name="question_id_right",
        )
    wrong_questions = models.ManyToManyField(
            Question,
            blank=True,
            related_name="question_id_wrong",
        )

