from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import (
    register,
    CardCreateView,
    ClasseurDetailView,
    CardListView,
    CardFormView,
    login_view
)

urlpatterns = [
                  path("", views.welcome_page_view, name="welcome"),
                  path('create-cards/', views.create_cards_view, name='create_cards'),
                  path("explore/", views.explore_view, name='explore'),
                  path("start-cards/", views.start_cards_view, name='start_cards'),

                  # Updated card creation and form view paths
                  path('classeur/<int:classeur_id>/card/create/', CardCreateView.as_view(), name='card_create'),
                  path('classeur/<int:classeur_id>/card/<int:pk>/edit/', CardFormView.as_view(), name='card_form'),

                  path('card-form/<int:classeur_id>/', CardFormView.as_view(), name='card_form'),
                  path("card-list/", CardListView.as_view(), name='card-list'),
                  path("edit/<int:pk>/", views.CardUpdateView.as_view(), name="card-update"),
                  path("card/<int:pk>/delete/", views.card_delete, name="card-delete"),

                  path('classeurs/', views.classeur_list, name='classeur_list'),
                  path('classeur/<int:pk>/', views.classeur_detail, name='classeur_detail'),
                  path('classeur/nouveau/', views.classeur_create, name='classeur_create'),
                  path('classeur/<int:pk>/modifier/', views.classeur_edit, name='classeur-edit'),
                  path('classeur/<int:pk>/supprimer/', views.classeur_delete, name='classeur_delete'),
                  path('classeur/<int:pk>/', ClasseurDetailView.as_view(), name='classeur-detail'),

                  path('login/', login_view, name='login'),
                  path('register/', register, name='register'),

                  # Other views...
                  path('classeur-All/', views.classeur_all_view, name='classeurAll'),
                  path('classeur-Eng/', views.classeur_eng_view, name='classeurEng'),
                  path('classeur-Esp/', views.classeur_esp_view, name='classeurEsp'),
                  path('classeur-Ita/', views.classeur_ita_view, name='classeurIta'),

                  path('voc-all1/', views.voc_all1_view, name='voc_all1'),
                  path('voc-all2/', views.voc_all2_view, name='voc_all2'),

                  path('retour/', views.retour, name='retour'),
                  path('sans-connection/', views.sans_connections_view, name='sans-connection'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
