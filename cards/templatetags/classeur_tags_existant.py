from django import template
from cards.models import BOXES, Card, Classeur

register = template.Library()

@register.inclusion_tag("cards/classeur_box_links_existante.html")
def classeur_boxes_as_links_existing(classeur):
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.filter(classeur=classeur, box=box_num).count()
        boxes.append({
            "number": box_num,
            "card_count": card_count,
        })
    return {"classeur": classeur, "boxes": boxes}