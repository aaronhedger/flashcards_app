import os
from audioop import reverse

from collections import defaultdict

import random
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


def voc_all2_view(request):
    flashcards = Flashcard.objects.all()

    card_data = [
        {'title': 'German Voc 1', 'front_content': 'der Vater', 'back_content': 'the father', 'index': 1},
        {'title': 'German Voc 2', 'front_content': 'die Mutter', 'back_content': 'the mother', 'index': 2},
        {'title': 'German Voc 3', 'front_content': 'der Sohn', 'back_content': 'the son', 'index': 3},
        {'title': 'German Voc 4', 'front_content': 'die Tochter', 'back_content': 'the daughter', 'index': 4},
        {'title': 'German Voc 5', 'front_content': 'die Großmutter', 'back_content': 'the grandmother', 'index': 5},
        {'title': 'German Voc 6', 'front_content': 'der Großvater', 'back_content': 'the grandfather', 'index': 6},
        {'title': 'German Voc 7', 'front_content': 'der Bruder', 'back_content': 'the brother', 'index': 7},
        {'title': 'German Voc 8', 'front_content': 'die Schwester', 'back_content': 'the sister', 'index': 8},
        {'title': 'German Voc 9', 'front_content': 'der Onkel', 'back_content': 'the uncle', 'index': 9},
        {'title': 'German Voc 10', 'front_content': 'die Tante', 'back_content': 'the aunt', 'index': 10},
        {'title': 'German Voc 11', 'front_content': 'der Neffe', 'back_content': 'the nephew', 'index': 11}
        ###{'title': 'German Voc 12', 'front_content': 'die Nichte', 'back_content': 'the niece', 'index': 1},
        ## {'title': 'German Voc 13', 'front_content': 'der Cousin', 'back_content': 'the cousin (male)', 'index': 1},
        #{'title': 'German Voc 14', 'front_content': 'die Cousine', 'back_content': 'the cousin (female)', 'index': 1},
        #{'title': 'German Voc 15', 'front_content': 'die Enkelin', 'back_content': 'the granddaughter', 'index': 1},
        #{'title': 'German Voc 16', 'front_content': 'der Enkel', 'back_content': 'the grandson', 'index': 1},
        #{'title': 'German Voc 17', 'front_content': 'die Schwiegermutter', 'back_content': 'the mother-in-law', 'index': 1},
        #{'title': 'German Voc 18', 'front_content': 'der Schwiegervater', 'back_content': 'the father-in-law', 'index': 1},
        # {'title': 'German Voc 19', 'front_content': 'die Schwiegertochter', 'back_content': 'the daughter-in-law', 'index': 1},
        # {'title': 'German Voc 20', 'front_content': 'der Schwiegersohn', 'back_content': 'the son-in-law', 'index': 1},
    ]

    total_cards = len(card_data)
    card_reappear = {i: None for i in range(total_cards)}
    print("----------------", card_reappear, os.getcwd())
    categorized_cards = []
    current_round = 1

    # Vérifier si un choix a été fait et le traiter
    if request.method == 'POST':
        card_index = int(request.POST.get('card_index'))

        choice = request.POST.get('choice')

        # Marquer la carte comme catégorisée
        categorized_cards.append(card_index)

        # Déterminer quand la carte doit réapparaître
        if choice == 'a':
            card_reappear[card_index] = current_round + 1
        elif choice == 'b':
            card_reappear[card_index] = current_round + 2
        elif choice == 'c':
            card_reappear[card_index] = current_round + 3
        elif choice == 'd':
            card_reappear[card_index] = current_round + 4

    while True:
        current_round_cards = []

        # Ajouter des cartes réapparaissant ce round
        for index, next_round in card_reappear.items():
            if next_round == current_round:
                current_round_cards.append(card_data[index])

        while len(current_round_cards) < 9:
            if len(categorized_cards) == total_cards:
                break

            for index in range(total_cards):
                if index not in categorized_cards and not any(
                        data.get('index') == index for data in current_round_cards if data.get('index') is not None):
                    current_round_cards.append(card_data[index])
                    if len(current_round_cards) >= 9:
                        break

        if not current_round_cards:
            break

        current_round += 1

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(card_data, 9)
    current_page = paginator.get_page(page_number)

    return render(request, 'cards/existing_classeur/classeur_sujet/voc_all2.html',
                  {'card_data': current_page, 'audio_file_path': '/path/to/audio/file', 'paginator': paginator})


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
