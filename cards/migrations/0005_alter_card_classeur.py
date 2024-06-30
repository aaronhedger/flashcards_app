# Generated by Django 4.0.4 on 2024-06-30 21:56

import cards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards','0004_alter_card_answer_alter_card_question_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='classeur',
            field=models.ForeignKey(default=cards.models.get_default_classeur, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.classeur'),
        ),
    ]