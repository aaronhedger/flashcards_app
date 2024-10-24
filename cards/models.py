from django.contrib.auth.models import User
from django.db import models

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)


class Classeur(models.Model):
    name = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Classeur asso. avec un utilisateur

    def __str__(self):
        return self.name


# fonction pour créer ou get un default classeur
def get_default_classeur(user=None):
    if user:
        default_classeur, _ = Classeur.objects.get_or_create(name='Default Classeur', user=user)
        return default_classeur.id


# Define the Card model
class Card(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],  # Default box for new cards is box 1
    )
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp of card creation

    # lien entre cartes et classeur et utilisateur
    classeur = models.ForeignKey(Classeur, on_delete=models.CASCADE, related_name='cards', default=get_default_classeur)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Default user

    def __str__(self):
        return self.question

    def move(self, solved):  # fonctionnement des boites, comment les cartes se déplacent en fonctions du choix
        new_box = self.box + 1 if solved else BOXES[0]

        if new_box in BOXES:
            self.box = new_box
            self.save()

        return self


class Flashcard(models.Model):
    front_content = models.CharField(max_length=100) # avant de la carte
    back_content = models.CharField(max_length=100) # arrière de la carte

    def __str__(self):
        return self.front_content  # Ajouter une méthode pour afficher le contenu de la carte
