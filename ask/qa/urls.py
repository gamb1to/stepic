from django.conf.urls import url, include
from django.contrib import admin

from qa.views import test
from qa.views import new_quest_func
from qa.views import one_quest_func
from qa.views import pop_quest_func
from qa.views import ask_func


urlpatterns = [
    url(r'^$', new_quest_func),
    url(r'^login/', test),
    url(r'^signup/', test),
    url(r'^question/(?P<id>\d+)/', one_quest_func),
    url(r'^ask/', ask_func, name='ask'),
    url(r'^popular/', pop_quest_func),
    url(r'^new/', test),
    ]

