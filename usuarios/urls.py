from django.urls import path
from .views import LoginAPIView, CadastroAPIView, LogoutAPIView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/cadastro/', CadastroAPIView.as_view(), name='api_cadastro'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
]
