from django.conf.urls import url
from jeopardy.views import (
    QuestionList,
    QuestionById,
    QuestionRandom,
    PlayerList,
    PlayerByName,
    PlayerById,
)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^questions/$', QuestionList.as_view()),
    url(r'^questions/id/(?P<pk>[0-9]+)/$', QuestionById.as_view()),
    url(r'^questions/random/$', QuestionRandom.as_view()),
    url(r'^players/$', PlayerList.as_view()),
    url(r'^players/name/(?P<name>.+)/$', PlayerByName.as_view()),
    url(r'^players/id/(?P<pk>[0-9]+)/$', PlayerById.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)