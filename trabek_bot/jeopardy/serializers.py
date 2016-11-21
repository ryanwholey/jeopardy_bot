from rest_framework import serializers
from jeopardy.models import (
    Player,
    Question,
)

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'score',
            'asked',
            'wrong_questions',
            'right_questions',
        )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'category',
            'air_date',
            'question',
            'answer',
            'value',
            'jeopardy_round',
            'show',
        )
