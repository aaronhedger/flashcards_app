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
    login_view,
    CardListExistingView
)

urlpatterns = [
                  path("", views.welcome_page_view, name="welcome"),
                  path('create-cards/', views.bibliothèque_view, name='bibliothèque'),
                  path("explore/", views.explore_view, name='explore'),
                  path("start-cards/", views.start_cards_view, name='start_cards'),

                  path('classeur/<int:classeur_id>/card/create/', views.CardCreateView.as_view(), name='card_create'),
                  path('classeur/nouveau/', views.classeur_create, name='classeur_create'),
                  path('create-public-classeur/',views.public_classeur_create, name='public_classeur_create'),
                  path('classeur/public/<int:pk>/', views.classeur_detail_public, name='classeur_detail_public'),


                  path('classeur/<int:pk>/modifier/', views.classeur_edit, name='classeur-edit'),
                  path('classeur/<int:pk>/supprimer/', views.classeur_delete, name='classeur_delete'),
                  path('classeurs/', views.classeur_list, name='classeur_list'),

                  path('classeur/<int:pk>/', ClasseurDetailView.as_view(), name='classeur_detail'),
                  path('admin/classeur/<int:pk>/', views.classeur_detail_admin, name='classeur_detail_admin'),

                  path("classeur/<int:classeur_id>/card/create/",views.CardCreateView.as_view(),name="card-create"),
                  path('classeur/<int:classeur_id>/cards/', CardListView.as_view(), name='card-list'),
                  path('classeur/public/<int:classeur_id>/cards/', CardListExistingView.as_view(), name='card-list-existante'),

                  path('classeur/<int:classeur_id>/cards/', views.card_list, name='card_list'),

                  path("edit/<int:pk>/", views.CardUpdateView.as_view(), name="card-update"),
                  path("delete/<int:pk>/", views.card_delete, name="card-delete"),

                  path("classeur/<int:classeur_id>/box/<int:box_num>/", views.ClasseurBoxView.as_view(),
                       name="classeur-box"),
                  path("classeur/public/<int:classeur_id>/box/<int:box_num>/", views.ClasseurBoxExistingView.as_view(),
                       name="classeur-box-existing"),


                  path('login/', login_view, name='login'),
                  path('register/', register, name='register'),

                  # Other views...
                  path('classeur-All/', views.classeur_all_view, name='classeurAll'),
                  path('classeur-Eng/', views.classeur_eng_view, name='classeurEng'),
                  path('classeurs/espagnol/', views.classeur_esp_view, name='classeurEsp'),
                  path('classeur-Ita/', views.classeur_ita_view, name='classeurIta'),

                  path('voc-all1/', views.voc_all1_view, name='voc_all1'),
                  path('voc-all2/', views.voc_all2_view, name='voc_all2'),
                  path('exercise-complete/', views.exercise_complete_view, name='exercise_complete'),

                  path('retour/', views.retour, name='retour'),
                  path('sans-connection/', views.sans_connections_view, name='sans-connection'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
