import random
from audioop import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Classeur
from .forms import ClasseurForm
from django.shortcuts import render
from .models import Flashcard
from .models import Card
from .forms import CardForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)


def welcome_page_view(request):
    return render(request,
                  "cards/welcome.html")  # Replace 'your_app/welcome.html' with the correct path to your welcome template


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
    audio_file_path = '/static/page-turn.wav'  # Replace this with the actual path to your audio file
    return render(request, 'cards/existing_cards.html', {'card_data': card_data, 'audio_file_path': audio_file_path})


def create_cards_view(request):
    # Logic to process the request (if needed)
    # Render the welcome page template
    return render(request,
                  'cards/base.html')  # Replace 'your_app/welcome.html' with the correct path to your welcome template


def explore_view(request):
    # Logique de la vue
    return render(request, 'cards/explore.html')


def start_cards_view(request):
    # Logique de la vue
    classeurs = Classeur.objects.all()
    return render(request, 'cards/start_cards.html', {'classeurs': classeurs})


class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-create")


class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("box", "-date_created")
    template_name = 'cards/card_list.html'
    context_object_name = 'card_list'


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")


def classeur_list(request):
    classeurs = Classeur.objects.all()
    return render(request, 'cards/classeur_list.html', {'classeurs': classeurs})


def classeur_detail(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk)
    return render(request, 'cards/classeur_detail.html', {'classeur': classeur})


def classeur_create(request):
    if request.method == "POST":
        form = ClasseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classeur_list')
    else:
        form = ClasseurForm()
    return render(request, 'cards/classeur_form.html', {'form': form})


def classeur_edit(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk)
    if request.method == "POST":
        form = ClasseurForm(request.POST, instance=classeur)
        if form.is_valid():
            form.save()
            return redirect('classeur_detail', pk=classeur.pk)
    else:
        form = ClasseurForm(instance=classeur)
    return render(request, 'cards/classeur_form.html', {'form': form, 'classeur': classeur})


def classeur_delete(request, pk):
    classeur = get_object_or_404(Classeur, pk=pk)
    if request.method == "POST":
        classeur.delete()
        return redirect('classeur_list')
    return render(request, 'cards/classeur_confirm_delete.html', {'classeur': classeur})


def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    classeur = card.classeur
    if request.method == "POST":
        card.delete()
        return redirect("card_list")
    return render(request, "cards/cards_confirm_delete.html", {'card': card, "classeur": classeur})
