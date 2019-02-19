from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def test(request, *args, **kwargs):
    return HttpResponse('200 OK\n' + '\n'.join(request.META['QUERY_STRING'].split('&')), content_type='text/plain')


def question_page(request, id):
    question = Question.objects.get(id=id)
    return render(request, 'question.html', {'question': question})
