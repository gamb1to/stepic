from django.http import HttpResponse 
from django.views.decorators.http import require_GET
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from qa.models import Question


def test(request, *args, **kwargs):
    return HttpResponse('OK')


@require_GET
def quest_func(request, query_set_returner, title):
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        raise Http404

    questions = query_set_returner()
    limit = 10
    
    paginator = Paginator(questions, limit)

    try:
        page = paginator.page(page)
    except:
        raise Http404

    
    page.base_url = '/question/'
    page.title = title

    return render(request, 'index.html', {
                'page': page
                })

    
new_quest_func = lambda request: quest_func(request, Question.objects.new, 'New')
pop_quest_func = lambda request: quest_func(request, Question.objects.popular, 'Popular')


def one_quest_func(request, id):
    try:
        question = Question.objects.get(pk=id)
    except:
        raise Http404

    answers = question.answer_set.all()[:]

    return render(request, 'question.html', {
                'question' : question,
                'answers' : answers,
                })















