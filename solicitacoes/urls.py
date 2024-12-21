from django.urls import path
from . import views


urlpatterns = [
   path('<id_solicitacao>/', views.index, name='index'),
   path('solicitacao/nova/', views.criar_solicitacao, name='criar_solicitacao'),
]