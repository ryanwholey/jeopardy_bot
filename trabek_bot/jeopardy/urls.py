from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from jeopardy.views import (
    QuestionList,
    QuestionById,
    QuestionRandom,
    PlayerList,
    PlayerByName,
    PlayerById,
    PlayerQuestionById,
    PlayerQuestionByName,
)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^questions/$', QuestionList.as_view()),
    url(r'^questions/id/(?P<pk>[0-9]+)/$', QuestionById.as_view()),
    url(r'^questions/random/$', QuestionRandom.as_view()),
    url(r'^players/$', PlayerList.as_view()),
    url(r'^players/name/(?P<name>.+)/$', PlayerByName.as_view()),
    url(r'^players/id/(?P<pk>[0-9]+)/$', PlayerById.as_view()),
    url(r'^players/name/(?P<name>.+)/question/(?P<question_id>[0-9]+)/$', PlayerQuestionByName.as_view()),
    url(r'^players/id/(?P<player_id>[0-9]+)/question/(?P<question_id>[0-9]+)/$', PlayerQuestionById.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
