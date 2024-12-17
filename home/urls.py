from django.urls import path
from home.views import lista_solicitacoes, home

urlpatterns = [
   path('solicitacoes/', lista_solicitacoes, name='lista_solicitacoes'),
   path('home', home, name='home')
]