from django import forms


class AskForm(forms.Form):
    title = forms.CharField(max_length=50)
    text = forms.CharField()


class AnswerForm(forms.Form):
    text = forms.CharField()


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
