from django.http import HttpResponse
from django.http import HttpResponseRedirect 
from django.views.decorators.http import require_GET
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from qa.models import Question

from qa.forms import AskForm
from qa.forms import AnswerForm


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

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(question)
            url = '/question/%d/' % (question.pk,)
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()

    form.url = '/question/%d/' % (question.pk,)
    return render(request, 'question.html', {
                'question' : question,
                'answers' : answers,
                'form' : form,
                })


def ask_func(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = '/question/%d/' % (question.pk,)
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'forms/form.html', {
                'form': form
                })













