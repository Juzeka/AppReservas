from django.urls import path
from . import views
from core.views import home


urlpatterns = [
    path('', views.login, name= 'login'),
    path('create', views.create, name= 'create'),
    path('logout', views.logout, name= 'logout'),
    path('reserva', home, name= 'reserva'),
]
