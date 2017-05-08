import datetime
from hashlib import md5

from django.http import HttpResponse
from django.http import HttpResponseRedirect 
from django.views.decorators.http import require_GET
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from qa.models import Question
from qa.models import Session
from qa.models import User

from qa.forms import AskForm
from qa.forms import AnswerForm
from qa.forms import UserForm


def test(request, *args, **kwargs):
    s = 'Username: %s<br>Session: %s\n'
    sessionid = request.COOKIES.get('sessionid', None)
    if sessionid:
        try:
            session = Session.objects.get(key=sessionid)
            sid = session.key
            username = session.user.username
            s = s % (username, sid)
        except Exception as e:
            s = str(e)
    else:
        s = 'No cookies'
    return HttpResponse(s)


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
            try:
                sessionid = request.COOKIES['sessionid']
                print('sessionid', sessionid)
                session = Session.objects.get(key=sessionid)
                print(session.user.username)
                answer.author = session.user
                answer.save()
            except:
                pass
            url = '/question/%d/' % (question.pk,)
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()

    form.url = '/question/%d/' % (question.pk,)
    return render(request, 'question.html', {
                'question': question,
                'answers': answers,
                'form': form,
                })


def ask_func(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            try:
                sessionid = request.COOKIES['sessionid']
                session = Session.objects.get(key=sessionid)
                question.author = session.user
                question.save()
            except:
                pass
            url = '/question/%d/' % (question.pk,)
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'forms/form.html', {
                'form': form
                })


##################################
def signup(request):
    if request.method == 'GET':
        form = UserForm()
        form.url = 'signup/'
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            session = Session()
            session.key = generate_long_random_key()
            session.user = user
            session.expires = datetime.datetime.now() + datetime.timedelta(days=5)
            session.save()
            response = HttpResponseRedirect('/')
            response.set_cookie('sessionid', session.key,
                                # domain='*',
                                # httponly=True,
                                expires=session.expires
                                )
            return response
    return render(request, 'signup.html', {
        'form': form
    })


def login(request):
    error = ''
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            session = do_login(username, password)
            if session:
                response = HttpResponseRedirect('/')
                response.set_cookie('sessionid', session.key,
                                    # domain='*',
                                    # httponly=True,
                                    expires=session.expires
                                    )
                return response
            else:
                error = u'Password or login is incorrect'
        except:
            error = u'Incorrect login/pass'

    return render(request, 'login.html', {'error': error})


def do_login(login, password):
    try:
        user = User.objects.get(username=login)
    except:
        return None
    hashed_pass = md5(password).hexdigest()
    if user.password != hashed_pass:
        return None
    session = Session()
    session.key = generate_long_random_key()
    session.user = user
    session.expires = datetime.datetime.now() + datetime.timedelta(days=5)
    session.save()
    return session


def generate_long_random_key(length=25):
    import random
    alphabet = '1234567890qwertyuiopasdfghjklzxcvbnm'
    return ''.join([random.choice(alphabet) for _ in range(length)])











