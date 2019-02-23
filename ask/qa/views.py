from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage

from .models import *
from .forms import *


def test(request, *args, **kwargs):
    return HttpResponse('200 OK\n' + '\n'.join(request.META['QUERY_STRING'].split('&')), content_type='text/plain')


def question_page(request, id):
    sessid = request.COOKIES['sessionid']
    session = Session.objects.get(key=sessid)
    user = session.user
    try:
        question = Question.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404
    # or question = get_object_or_404(Question, id=id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer(**form.cleaned_data, question=question, author=user)
            answer.save()
            return HttpResponseRedirect('/question/{}/'.format(id))
    else:
        form = AnswerForm()

    answers = question.answer_set.all()

    return render(request, 'question.html', {'question': question, 'answers': answers, 'form': form})


def question_list_all(request):
    questions = Question.objects.new()
    limit = 2
    paginator = Paginator(questions, limit)

    page = request.GET.get('page', 1)
    page = paginator.page(page)

    try:
        next_page = page.next_page_number()
    except EmptyPage:
        next_page = None

    return render(request, 'question_list.html', {'questions': page.object_list, 'next': next_page})


def question_list_popular(request):
    questions = Question.objects.popular()
    limit = 10
    paginator = Paginator(questions, limit)

    page = request.GET.get('page', 1)
    page = paginator.page(page)

    try:
        next_page = page.next_page_number()
    except EmptyPage:
        next_page = None

    return render(request, 'question_list_popular.html', {'questions': page.object_list, 'page': page, 'next': next_page})


def question_add(request):
    sessid = request.COOKIES['sessionid']
    session = Session.objects.get(key=sessid)
    user = session.user
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = Question(**form.cleaned_data, author=user)
            question.save()
            return HttpResponseRedirect('/question/{}/'.format(question.id))
    else:
        form = AskForm()

    return render(request, 'question_add.html', {'form': form})


def random_string():
    import string
    import random

    s = string.ascii_letters + string.digits
    result = ''.join(random.choice(s) for _ in range(random.randint(10, 20)))
    return result


def do_login(username, password):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None

    if user.password != password:
        return None

    session = Session.objects.create(key=random_string(), user=user)
    return session.key


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user = User(username=username, password=password)
            new_user.save()

            sessid = do_login(username, password)
            response = HttpResponseRedirect('/')
            response.set_cookie('sessionid', sessid)
            return response
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            sessid = do_login(username, password)

            if sessid:
                response = HttpResponseRedirect('/')
                response.set_cookie('sessionid', sessid)
                return response
            else:
                error = 'Wrong login / password'
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})
