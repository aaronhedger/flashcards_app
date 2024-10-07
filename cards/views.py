import json
from django.urls import reverse

from django.http import JsonResponse

from collections import defaultdict
from django.shortcuts import render, redirect
from .models import Card
from .algorithms import flashcard_algorithm  # Assurez-vous d'importer votre algorithme

from django.views.decorators.http import require_POST

import random

from .algorithms import flashcard_algorithm

from lib2to3.fixes.fix_input import context

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DetailView, FormView,
)

from .forms import CardForm
from .forms import ClasseurForm, SignUpForm
from .models import Card, Flashcard
from .models import Classeur


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


def flashcard_view(request):
    # Initialisation
    rounds_to_reappear = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    categorized_cards = {}  # Dictionnaire pour stocker les comptes de cartes classées
    card_reappear = {}  # Dictionnaire pour gérer la réapparition des cartes
    card_data = list(Flashcard.objects.all())  # Récupère toutes les cartes de la base de données

    # Gestion des choix utilisateur
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        category = request.POST.get("category")

        if card_id and category:
            # Met à jour le round de réapparition de la carte selon le choix
            reappear_round = rounds_to_reappear[category]
            card_reappear[card_id] = reappear_round

            # Si 'd' est choisi, incrémenter le compteur pour cette carte
            if category == 'd':
                categorized_cards[card_id] = categorized_cards.get(card_id, 0) + 1

    # Vérifie si toutes les cartes ont été catégorisées 'd' deux fois
    if all(categorized_cards.get(card.id, 0) >= 2 for card in card_data):
        return render(request,
                      'cards/existing_classeur/classeur_sujet/exercise_complete.html')  # Ou une autre page pour dire qu'il n'y a plus de cartes à afficher
    # Redirige vers une page de fin si toutes les cartes sont classées

    # Logique pour choisir la carte actuelle à afficher
    current_card = None

    for card in card_data:
        if card.id not in card_reappear or card_reappear[card.id] <= 0:
            current_card = card
            break

    # Si aucune carte n'est trouvée à afficher, on peut gérer ce cas (peut-être rediriger ou afficher un message)
    if not current_card:
        return render(request,
                      'cards/existing_classeur/classeur_sujet/exercise_complete.html')  # Ou une autre page pour dire qu'il n'y a plus de cartes à afficher

    context = {
        'card': current_card,
        'audio_file_path': 'path/to/audio.mp3',  # Assure-toi que ce chemin est correct
    }

    return render(request, 'cards/existing_classeur/classeur_sujet/voc_all2.html', context)


card_data = [
    {"index": 1, "title": "German Voc 1", "front_content": "der Vater", "back_content": "the father"},
    {"index": 2, "title": "German Voc 2", "front_content": "die Mutter", "back_content": "the mother"},
    {"index": 3, "title": "German Voc 3", "front_content": "der Sohn", "back_content": "the son"},
    {"index": 4, "title": "German Voc 4", "front_content": "die Tochter", "back_content": "the daughter"},
    {"index": 5, "title": "German Voc 5", "front_content": "die Großmutter", "back_content": "the grandmother"},
    {"index": 6, "title": "German Voc 6", "front_content": "der Großvater", "back_content": "the grandfather"},
    {"index": 7, "title": "German Voc 7", "front_content": "der Bruder", "back_content": "the brother"},
    {"index": 8, "title": "German Voc 8", "front_content": "die Schwester", "back_content": "the sister"},
    {"index": 9, "title": "German Voc 9", "front_content": "der Onkel", "back_content": "the uncle"},
    {"index": 10, "title": "German Voc 10", "front_content": "die Tante", "back_content": "the aunt"},
    {"index": 11, "title": "German Voc 11", "front_content": "der Neffe", "back_content": "the nephew"},
    {"index": 12, "title": "German Voc 12", "front_content": "die Nichte", "back_content": "the niece"},
    {"index": 13, "title": "German Voc 13", "front_content": "der Cousin", "back_content": "the cousin (male)"},
    {"index": 14, "title": "German Voc 14", "front_content": "die Cousine", "back_content": "the cousin (female)"},
    {"index": 15, "title": "German Voc 15", "front_content": "die Enkelin", "back_content": "the granddaughter"},
    {"index": 16, "title": "German Voc 16", "front_content": "der Enkel", "back_content": "the grandson"},
    {"index": 17, "title": "German Voc 17", "front_content": "die Schwiegermutter",
     "back_content": "the mother-in-law"},
    {"index": 18, "title": "German Voc 18", "front_content": "der Schwiegervater",
     "back_content": "the father-in-law"}
]
current_card_data = []  # Une variable pour stocker les cartes en cours d'affichage


def voc_all2_view(request):
    cards = Card.objects.all()
    global current_card_data  # Utiliser la variable globale pour suivre les cartes

    if request.method == "POST":
        card_id = request.POST.get("card_id")
        category = request.POST.get("category")

        # Traitez le choix de l'utilisateur
        user_choices = {int(card_id): category}

        # Utiliser l'algorithme pour obtenir la prochaine série de cartes
        next_cards = flashcard_algorithm(current_card_data, user_choices)

        # Si next_cards est vide, cela signifie que toutes les cartes ont été classées
        if not next_cards:
            return render(request,
                          'cards/existing_classeur/classeur_sujet/exercise_complete.html')  # Rediriger vers une page de fin ou de récapitulatif

        # Récupérer la prochaine carte à afficher
        current_card_data = next_cards  # Mettez à jour la variable pour la prochaine série de cartes
        return render(request, 'cards/existing_classeur/classeur_sujet/voc_all2.html',
                      {'card': current_card_data[0]})  # Passer la première carte à la vue

    # Pour le premier chargement de la page, récupérer toutes les cartes
    current_card_data = list(
        Card.objects.all().values('index', 'question', 'answer'))  # Récupérez toutes les cartes disponibles
    if current_card_data:  # S'il y a des cartes disponibles
        initial_card = current_card_data[0]  # Prendre la première carte
    else:
        return render(request,
                      'cards/existing_classeur/classeur_sujet/exercise_complete.html')  # Pas de cartes disponibles, rediriger vers une page de fin

    return render(request, 'cards/existing_classeur/classeur_sujet/voc_all2.html',
                  {'card': cards})  # Passer la carte initiale à la vue


@login_required
def create_cards_view(request):
    return render(request, 'cards/base.html')


@login_required
def explore_view(request):
    classeurs = Classeur.objects.filter(user=request.user)
    return render(request, 'cards/explore.html', {'classeurs': classeurs})


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


def view_classeur(request, classeur_id):
    classeur = Classeur.objects.get(id=classeur_id)
    cards = Card.objects.all()
    return render(request, 'cards/view_classeur.html', {'classeur': classeur, 'card': cards})

@login_required
def explore_view(request):
    classeurs = Classeur.objects.filter(user=request.user)  # Récupérer tous les classeurs de l'utilisateur

    return render(request, 'cards/explore.html', {'classeurs': classeurs})

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

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user).order_by("classeur", "box", "-date_created")


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")


@login_required
def classeur_list(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page or handle it as needed

    classeurs = Classeur.objects.filter(user=request.user)
    return render(request, 'cards/classeur_list.html', {'classeurs': classeurs})


@login_required
def classeur_detail(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk, user=request.user)
    return render(request, 'cards/classeur_detail.html', {'classeur': classeur})

    # Tu peux ajouter de la logique ici pour le tutoriel (par exemple, démarrer le jeu de flashcards)
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


def classeur_all_view(request):
    return render(request, "cards/existing_classeur/classeurAll.html")


def classeur_eng_view(request):
    return render(request, "cards/existing_classeur/classeurEng.html")


def classeur_esp_view(request):
    return render(request, "cards/existing_classeur/classeurEsp.html")


def classeur_ita_view(request):
    return render(request, "cards/existing_classeur/classeurIta.html")


def retour(request):
    return render(request, "cards/sans_connection.html")


def voc_all1_view(request):
    return render(request, "cards/existing_classeur/classeur_sujet/voc_all1.html")


def sans_connections_view(request):
    return render(request, 'cards/sans_connection.html')


def exercise_complete_view(request):
    return render(request, 'cards/existing_classeur/classeur_sujet/exercise_complete.html')
