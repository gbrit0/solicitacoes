from django.urls import path
from solicitacoes.views import criar_solicitacao, apagar_solicitacao



urlpatterns = [
   path('cadastrar_solicitacao', criar_solicitacao, name='criar_solicitacao'),
   path('solicitacao/apagar/<str:num_solicitacao>/', apagar_solicitacao, name='apagar_solicitacao')
]