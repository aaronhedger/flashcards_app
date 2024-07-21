# cards/models.py
from django.contrib.auth.models import User

from django.db import models


class Classeur(models.Model):
    name = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def get_default_classeur():
    default_classeur, _ = Classeur.objects.get_or_create(name='Default Classeur')
    return default_classeur.id


class Card(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    classeur = models.ForeignKey(Classeur, on_delete=models.CASCADE, related_name='cards', default=get_default_classeur)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.question

    def move(self, solved):
        pass  # Implement any logic if needed


class Flashcard(models.Model):
    front_content = models.CharField(max_length=100)
    back_content = models.CharField(max_length=100)
