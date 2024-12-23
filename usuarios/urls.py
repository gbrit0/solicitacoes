from django.urls import path
from usuarios.views import login, cadastro, logout

urlpatterns = [
   path('login/', login, name='login'),
   path('logout', logout, name='logout'),
   path('cadastro', cadastro, name='cadastro'),
   path('', login, name='login')
]