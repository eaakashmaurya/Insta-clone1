from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path(
        route='sandhi/',
        view=views.sandhi,
        name='sandhi'
    ),

    path(
        route='dictionary/',
        view=views.dictionary,
        name='dictionary'
    ),

    path(
        route='sandhi-splitter/',
        view=views.sandhi_splitter,
        name='sandhi_splitter'
    ),

    path(
        route='resources/',
        view=views.resources,
        name='resources'
    ),
]