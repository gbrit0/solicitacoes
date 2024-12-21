from django.urls import path
from home.views import lista_solicitacoes, home, cadastrar_solicitacao

urlpatterns = [
   path('home', home, name='home'),
   path('lista_solicitacoes', lista_solicitacoes, name='lista_solicitacoes'),
   path('cadastrar_solicitacao', cadastrar_solicitacao, name="cadastrar_solicitacao")
   
]