from django.urls import path
from home.views import lista_solicitacoes

urlpatterns = [
   path('lista_solicitacoes', lista_solicitacoes, name='lista_solicitacoes')
   
]