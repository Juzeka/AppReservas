from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name= 'home'),
    path('reservar', views.reservar, name= 'reservar'),
    path('comprovante', views.comprovante, name= 'comprovante'),
]
