from django.urls import path
from . import views


urlpatterns = [
   path('solicitacao/nova/', views.criar_solicitacao, name='criar_solicitacao'),
]