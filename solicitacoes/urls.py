from django.urls import path
from solicitacoes.views import criar_solicitacao, apagar_solicitacao, editar_solicitacao



urlpatterns = [
   path('cadastrar_solicitacao', criar_solicitacao, name='criar_solicitacao'),
   path('<str:num_solicitacao>/delete', apagar_solicitacao, name='delete'),
   path('editar_solicitacao/<str:c1_num>/', editar_solicitacao, name='editar_solicitacao'),
]