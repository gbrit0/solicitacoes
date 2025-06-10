from django.urls import path
from .views import LoginAPIView, CadastroAPIView, LogoutAPIView, EdicaoUsuarioAPIView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/cadastro/', CadastroAPIView.as_view(), name='api_cadastro'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/usuario/<str:cpf>/', EdicaoUsuarioAPIView.as_view(), name='api_editar_usuario'),
]
