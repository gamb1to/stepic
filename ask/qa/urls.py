from django.conf.urls import url

from qa.views import test
from qa.views import new_quest_func
from qa.views import one_quest_func
from qa.views import pop_quest_func
from qa.views import ask_func
from qa.views import signup
from qa.views import login


urlpatterns = [
    url(r'^$', new_quest_func),
    url(r'^login/', login),
    url(r'^signup/', signup),
    url(r'^question/(?P<id>\d+)/', one_quest_func),
    url(r'^ask/', ask_func, name='ask'),
    url(r'^popular/', pop_quest_func),
    url(r'^new/', test),
    ]

