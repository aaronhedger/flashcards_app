#views.py

import random
from audioop import reverse

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Classeur
from .forms import ClasseurForm, SignUpForm
from django.shortcuts import render
from .models import Flashcard
from .models import Card

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from .forms import CardForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DetailView, FormView,
)
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('login')  # Redirect to a success page or home
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('classeur_list')  # Redirect to the home page or wherever you want
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def welcome_page_view(request):
    return render(request, "cards/welcome.html")


def existing_cards_view(request):
    card_data = [
        {'title': 'Card 1', 'front_content': 'Quand s\'arrête la boucle définie par cette instruction? while a<=6',
         'back_content': 'Quand >6'},
        {'title': 'Card 2', 'front_content': 'Front content for card 2', 'back_content': 'Back content for card 2'},
        {
            'title': 'Card 3',
            'front_content': 'What is the output of the following code?<br/><pre><code>for i in range(5):<br/>&nbsp;&nbsp;&nbsp;&nbsp;print(i)</code></pre>',
            'back_content': '0<br/>1<br/>2<br/>3<br/>4'},
        {'title': 'German Voc 1', 'front_content': 'der Vater', 'back_content': 'the father'},
        {'title': 'German Voc 2', 'front_content': 'die Mutter', 'back_content': 'the mother'},
        {'title': 'German Voc 3', 'front_content': 'der Sohn', 'back_content': 'the son'},
        {'title': 'German Voc 4', 'front_content': 'die Tochter', 'back_content': 'the daughter'},
        {'title': 'German Voc 5', 'front_content': 'die Großmutter', 'back_content': 'the grandmother'},
        {'title': 'German Voc 6', 'front_content': 'der Großvater', 'back_content': 'the grandfather'},
        {'title': 'German Voc 7', 'front_content': 'der Bruder', 'back_content': 'the brother'},
        {'title': 'German Voc 8', 'front_content': 'die Schwester', 'back_content': 'the sister'},
        {'title': 'German Voc 9', 'front_content': 'der Onkel', 'back_content': 'the uncle'},
        {'title': 'German Voc 10', 'front_content': 'die Tante', 'back_content': 'the aunt'},
        {'title': 'German Voc 11', 'front_content': 'der Neffe', 'back_content': 'the nephew'},
        {'title': 'German Voc 12', 'front_content': 'die Nichte', 'back_content': 'the niece'},
        {'title': 'German Voc 13', 'front_content': 'der Cousin', 'back_content': 'the cousin (male)'},
        {'title': 'German Voc 14', 'front_content': 'die Cousine', 'back_content': 'the cousin (female)'},
        {'title': 'German Voc 15', 'front_content': 'die Enkelin', 'back_content': 'the granddaughter'},
        {'title': 'German Voc 16', 'front_content': 'der Enkel', 'back_content': 'the grandson'},
        {'title': 'German Voc 17', 'front_content': 'die Schwiegermutter', 'back_content': 'the mother-in-law'},
        {'title': 'German Voc 18', 'front_content': 'der Schwiegervater', 'back_content': 'the father-in-law'},
        {'title': 'German Voc 19', 'front_content': 'die Schwiegertochter',
         'back_content': 'the daughter-in-law'},
        {'title': 'German Voc 20', 'front_content': 'der Schwiegersohn', 'back_content': 'the son-in-law'},
    ]
    audio_file_path = '/static/page-turn.wav'
    return render(request, 'cards/existing_cards.html', {'card_data': card_data, 'audio_file_path': audio_file_path})


@login_required
def create_cards_view(request):
    return render(request, 'cards/base.html')


@login_required
def explore_view(request):
    return render(request, 'cards/explore.html')


@login_required
def start_cards_view(request):
    classeurs = Classeur.objects.filter(user=request.user)
    return render(request, 'cards/start_cards.html', {'classeurs': classeurs})

def card_form(request, classeur_id):
    classeur = get_object_or_404(Classeur, pk=classeur_id)
    # Your logic here
    return render(request, 'cards/card_form.html', {'classeur': classeur})


class ClasseurDetailView(DetailView):
    model = Classeur
    template_name = 'cards/classeur_cartes.html'  # Template à personnaliser
    context_object_name = 'classeur'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = self.object.cards.all()  # Récupérer toutes les cartes liées à ce classeur
        return context


class CardCreateView(CreateView):
    model = Card
    fields = ['question', 'answer']
    template_name = 'cards/card_form.html'  # Template à personnaliser

    def form_valid(self, form):
        user = self.request.user

        # Récupérer l'ID du classeur depuis l'URL
        classeur_id = self.kwargs['classeur_id']
        classeur = get_object_or_404(Classeur, id=classeur_id, user=user)

        # Associer la carte au classeur et à l'utilisateur
        form.instance.classeur = classeur
        form.instance.user = user

        return super().form_valid(form)


class CardFormView(FormView):
    form_class = CardForm
    template_name = 'cards/card_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classeur_id'] = self.kwargs.get('classeur_id')
        return context

    def form_valid(self, form):
        # Handle form submission
        card = form.save(commit=False)
        card.classeur_id = self.kwargs.get('classeur_id')
        card.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('card-list', kwargs=["card-list", self.object.id])  # Redirect after a successful form submission


class CardListView(ListView):
    model = Card
    template_name = 'cards/card_list.html'
    context_object_name = 'card_list'

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user).order_by("classeur", "-date_created")


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")


@login_required
def classeur_list(request):
    print(request.user)  # Debugging line
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page or handle it as needed

    classeurs = Classeur.objects.filter(user=request.user)
    return render(request, 'cards/classeur_list.html', {'classeurs': classeurs})


@login_required
def classeur_detail(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk, user=request.user)
    return render(request, 'cards/classeur_detail.html', {'classeur': classeur})


@login_required
def classeur_create(request):
    if request.method == "POST":
        form = ClasseurForm(request.POST)
        if form.is_valid():
            classeur = form.save(commit=False)
            classeur.user = request.user
            classeur.save()
            return redirect('classeur_list')
    else:
        form = ClasseurForm()
    return render(request, 'cards/classeur_form.html', {'form': form})


@login_required
def classeur_edit(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk, user=request.user)
    if request.method == "POST":
        form = ClasseurForm(request.POST, instance=classeur)
        if form.is_valid():
            form.save()
            return redirect('classeur_detail', pk=classeur.pk)
    else:
        form = ClasseurForm(instance=classeur)
    return render(request, 'cards/classeur_form.html', {'form': form, 'classeur': classeur})


@login_required
def classeur_delete(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk, user=request.user)
    if request.method == "POST":
        classeur.delete()
        return redirect('classeur_list')
    return render(request, 'cards/classeur_confirm_delete.html', {'classeur': classeur})


@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    if request.method == "POST":
        card.delete()
        return redirect("card_list")
    return render(request, "cards/cards_confirm_delete.html", {'card': card})
