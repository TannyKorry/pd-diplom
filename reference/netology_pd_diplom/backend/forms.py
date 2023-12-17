from allauth.account.forms import SignupForm
from allauth.account.views import AjaxCapableProcessFormViewMixin, RedirectAuthenticatedUserMixin
from django import forms
from django.views.generic import FormView

from .models import USER_TYPE_CHOICES, User


class CustomSignupForm(SignupForm):
    type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='Тип')
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    company = forms.CharField(max_length=30, label='Компания')
    position = forms.CharField(max_length=10, label='Должность')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['company'].required = False
        self.fields['position'].required = False

    def signup(self, request, user):
        user.type = self.cleaned_data['type']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.company = self.cleaned_data['company']
        user.position = self.cleaned_data['position']
        user.save()
        return user


class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

