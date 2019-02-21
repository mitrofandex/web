from django import forms
from .models import *


class AskForm(forms.Form):
    title = forms.CharField(max_length=50)
    text = forms.CharField()

    def clean(self):
        return self.cleaned_data
    #
    # def save(self):
    #     cleaned = self.cleaned_data
    #     question = Question(**cleaned)
    #     question.save()
    #     return question


class AnswerField(forms.Form):
    text = forms.CharField()
    question = None