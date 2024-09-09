# cards/forms.py


from django import forms
from .models import Classeur
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cards.models import Card


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']


class CardCheckForm(forms.Form):
    card_id = forms.IntegerField(required=True)
    solved = forms.BooleanField(required=False)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["question", "answer", "classeur"]


class ClasseurForm(forms.ModelForm):
    class Meta:
        model = Classeur
        fields = ["name"]
