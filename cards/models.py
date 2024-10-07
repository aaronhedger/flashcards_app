# cards/models.py
from django.contrib.auth.models import User

from django.db import models


class Classeur(models.Model):
    name = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def get_default_classeur(user=None):
    if user:
        default_classeur, _ = Classeur.objects.get_or_create(name='Default Classeur', user=user)
        return default_classeur.id


NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)


class Card(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    classeur = models.ForeignKey(Classeur, on_delete=models.CASCADE, related_name='cards', default=get_default_classeur)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.question


class Flashcard(models.Model):
    front_content = models.CharField(max_length=100)
    back_content = models.CharField(max_length=100)

    def __str__(self):
        return self.front_content  # Ajouter une méthode pour afficher le contenu de la carte
