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

    def get(self, request, *args, **kwargs):
        question = Question.objects.raw((
            "SELECT * FROM jeopardy_question AS r1 "
            "JOIN (SELECT CEIL(RAND() * "
            "(SELECT MAX(id) FROM jeopardy_question)) AS id) "
            "AS r2 WHERE r1.id >= r2.id "
            "ORDER BY r1.id ASC "
            "LIMIT 1"
        ))
        serializer = QuestionSerializer(question[0])
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerList(ListCreateAPIView):
    """
    List all players and post
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerByName(RetrieveUpdateDestroyAPIView):
    """
    Get player by name
    Used for read-write-delete endpoints to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'name'


class PlayerById(RetrieveUpdateDestroyAPIView):
    """
    Get player by id
    Used for read-write-delete endpoints to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_fields = 'pk'


















