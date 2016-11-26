from rest_framework import status
from rest_framework.response import Response
from jeopardy.models import (
    Question,
    Player,
)
from jeopardy.serializers import (
    QuestionSerializer,
    PlayerSerializer,
)
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)


class QuestionList(ListCreateAPIView):
    """
    Get all questions, please dont use on real data set
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category',)

class QuestionById(RetrieveUpdateDestroyAPIView):
    """
    Get question by id
    Used for read-write-delete endpoints to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'pk'


class QuestionRandom(GenericAPIView):

    """
    Get random question
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('player',)
    raw_random_sql = (
        "SELECT * FROM jeopardy_question AS r1 "
        "JOIN (SELECT CEIL(RAND() * "
        "(SELECT MAX(id) FROM jeopardy_question)) AS id) "
        "AS r2 WHERE r1.id >= r2.id "
        "ORDER BY r1.id ASC "
        "LIMIT 1"
    )

    def get(self, request, *args, **kwargs):
        question = Question.objects.raw(self.raw_random_sql)
        serializer = QuestionSerializer(question[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        question = Question.objects.raw(self.raw_random_sql)
        serializer = QuestionSerializer(question[0])

        # increase asked by one
        player_name = request.data.get('player')
        if player_name:
            player, was_created = Player.objects.get_or_create(name=player_name)
            player.asked = player.asked + 1
            player.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PlayerList(ListCreateAPIView):
    """
    List all players and post
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerByName(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Get player by name
    Used for read-write-delete endpoints to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'name'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'asked',
        'score',
        'correct',
        'incorrect',
    )

    def get(self, request, *args, **kwargs):
        player = Player.objects.get(name=kwargs['name'])
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        player = Player.objects.get(name=kwargs['name'])
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        player = Player.objects.get_or_create(name=kwargs['name'])[0]
        query_asked = request.query_params.get('asked')
        query_score = request.query_params.get('score')
        correct_question_id = request.query_params.get('correct')
        incorrect_question_id = request.query_params.get('incorrect')
        asked = player.asked
        score = player.score

        if query_asked:
            player.asked = asked + 1
        if query_score:
            try:
                query_score = int(query_score)
            except:
                Response(status=status.HTTP_400_BAD_REQUEST)
            player.score = score + query_score
        if correct_question_id:
            question = Question.objects.get(id=correct_question_id)
            player.right_questions.add(question)
            player.score = score + int(question.value)
        if incorrect_question_id:
            question = Question.objects.get(id=incorrect_question_id)
            player.wrong_questions.add(question)
            player.score = score - int(question.value)

        if query_score or query_asked or correct_question_id or incorrect_question_id:
            player.save()
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlayerById(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Get player by id
    Used for read-write-delete endpoints to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_fields = 'pk'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'asked',
        'score',
        'correct',
        'incorrect',
    )

    def get(self, request, *args, **kwargs):
        player = Player.objects.get(id=kwargs['pk'])
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        player = Player.objects.get(id=kwargs['pk'])
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        player = Player.objects.get(id=kwargs['pk'])
        query_asked = request.query_params.get('asked')
        query_score = request.query_params.get('score')
        correct_question_id = request.query_params.get('correct')
        incorrect_question_id = request.query_params.get('incorrect')
        asked = player.asked
        score = player.score
        if query_asked:
            player.asked = asked + 1
        if query_score:
            try:
                query_score = int(query_score)
            except:
                Response(status=status.HTTP_400_BAD_REQUEST)
            player.score = score + query_score
        if correct_question_id:
            question = Question.objects.get(correct_question_id)
            player.right_questions.add(question)
            player.score -= int(question.value)
        if incorrect_question_id:
            question = Question.objects.get(incorrect_question_id)
            player.wrong_questions.add(question)
            player.score -= int(question.value)
        if query_score or query_asked or correct_question_id or incorrect_question_id:
            player.save()
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlayerQuestionById(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('correct', )

    def patch(self, request, *args, **kwargs):
        player_id = self.kwargs.get('player_id', None)
        question_id = self.kwargs.get('question_id', None)
        if not player_id or not question_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.get(id=player_id)
        question = Question.objects.get(id=question_id)

        correct = request.query_params.get('correct', None)
        if not correct:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if correct:
            player.right_questions.add(question)
        else:
            player.wrong_questions.add(question)
        player.save()
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        player = Player.objects.get(id=kwargs.get('player_id'))
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlayerQuestionByName(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('correct',)

    def patch(self, request, *args, **kwargs):
        name = self.kwargs.get('name', None)
        question_id = self.kwargs.get('question_id', None)
        if not name or not question_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.get(name=name)
        question = Question.objects.get(id=question_id)

        correct = request.query_params.get('correct', None)
        if not correct:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if correct:
            player.right_questions.add(question)
        else:
            player.wrong_questions.add(question)
        player.save()
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        player = Player.objects.get(name=kwargs.get('name'))
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

