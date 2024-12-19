from django.urls import path
from home.views import lista_solicitacoes, home, solicitacao

urlpatterns = [
   path('home', home, name='home'),
   path('solicitacoes', lista_solicitacoes, name='lista_solicitacoes'),
   path('solicitacao', solicitacao, name='solicitacao')
]