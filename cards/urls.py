# cards/urls.py
from typing import List, Any
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from django.conf.urls.static import static
from . import views

urlpatterns = ([
    path("", views.welcome_page_view, name="welcome"),
    path('existing-cards/', views.existing_cards_view, name='existing_cards'),
    path('create-cards/', views.create_cards_view, name='create_cards'),
    path("explore/", views.explore_view, name='explore'),
    path("start-cards/", views.start_cards_view, name='start_cards'),
    path("card-form/", views.CardCreateView.as_view(), name='card_form'),
    path("card-list/", views.CardListView.as_view(), name='card-list'),
    path("edit/<int:pk>", views.CardUpdateView.as_view(), name="card-update"),
    path("card-create/", views.CardCreateView.as_view(), name="card-create"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))



