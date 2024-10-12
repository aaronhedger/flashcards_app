from django.contrib.auth.models import User
from django.db import models

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)


# Define the Classeur model
class Classeur(models.Model):
    name = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Classeur is associated with a user

    def __str__(self):
        return self.name


# Function to get or create a default Classeur for a user
def get_default_classeur(user=None):
    if user:
        default_classeur, _ = Classeur.objects.get_or_create(name='Default Classeur', user=user)
        return default_classeur.id


# Define the Card model
class Card(models.Model):
    question = models.CharField(max_length=100)  # The front side of the card (question)
    answer = models.CharField(max_length=100)  # The back side of the card (answer)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],  # Default box for new cards is box 1
    )
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp of card creation

    # Link each Card to a Classeur and User
    classeur = models.ForeignKey(Classeur, on_delete=models.CASCADE, related_name='cards', default=get_default_classeur)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Default user (to be handled later)

    def __str__(self):
        return self.question

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]

        if new_box in BOXES:
            self.box = new_box
            self.save()

        return self


class Flashcard(models.Model):
    front_content = models.CharField(max_length=100)
    back_content = models.CharField(max_length=100)

    def __str__(self):
        return self.front_content  # Ajouter une méthode pour afficher le contenu de la carte
