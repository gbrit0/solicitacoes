from django.urls import path
from solicitacoes.views import criar_solicitacao



urlpatterns = [
   path('cadastrar_solicitacao', criar_solicitacao, name='criar_solicitacao'),
]