# cards/urls.py
from django.contrib import admin
from typing import List, Any
from .views import register
from django.urls import path

from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from django.conf.urls.static import static
from . import views
from .views import login_view

urlpatterns = ([
    path("", views.welcome_page_view, name="welcome"),
    path('existing-cards/', views.existing_cards_view, name='existing_cards'),
    path('create-cards/', views.create_cards_view, name='create_cards'),
    path("explore/", views.explore_view, name='explore'),
    path("start-cards/", views.start_cards_view, name='start_cards'),
    path("card-form/", views.CardCreateView.as_view(), name='card_form'),
    path("card-list/", views.CardListView.as_view(), name='card-list'),
    path("edit/<int:pk>", views.CardUpdateView.as_view(), name="card-update"),
    path("card/<int:pk>/delete", views.card_delete, name="card-delete"),
    path("card-create/", views.CardCreateView.as_view(), name="card-create"),
    path('classeurs/', views.classeur_list, name='classeur_list'),
    path('classeur/<int:pk>/', views.classeur_detail, name='classeur_detail'),
    path('classeur/nouveau/', views.classeur_create, name='classeur_create'),
    path('classeur/<int:pk>/modifier/', views.classeur_edit, name='classeur-edit'),
    path('classeur/<int:pk>/supprimer/', views.classeur_delete, name='classeur_delete'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))



