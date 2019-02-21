from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage

from .models import *
from .forms import *


def test(request, *args, **kwargs):
    return HttpResponse('200 OK\n' + '\n'.join(request.META['QUERY_STRING'].split('&')), content_type='text/plain')


def question_page(request, id):
    try:
        question = Question.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404
    # or question = get_object_or_404(Question, id=id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer(**form.cleaned_data, question=question, author_id=1)
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
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = Question(**form.cleaned_data, author_id=1)
            question.save()
            return HttpResponseRedirect('/question/{}/'.format(question.id))
    else:
        form = AskForm()

    return render(request, 'question_add.html', {'form': form})
