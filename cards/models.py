# cards/models.py

from django.db import models

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)


#classeur

class Classeur(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


def get_default_classeur():
    default_classeur, _ = Classeur.objects.get_or_create(titre='Default Classeur')
    return default_classeur.id


class Card(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    classeur = models.ForeignKey(Classeur, on_delete=models.CASCADE, related_name='cards', default=get_default_classeur)

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
