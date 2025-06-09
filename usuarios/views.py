from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import LoginSerializer, CadastroSerializer

User = get_user_model()

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request=LoginSerializer, # Informa qual serializer define o corpo da requisição
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {
                        'type': 'string', 
                        'description': 'Usuário autenticado com sucesso!'
                    }
                }
            },
            400: {
                'description': 'Credenciais inválidas ou dados de requisição incorretos.'
            },
        },
        summary="Autentica um usuário.",
        description="Este endpoint recebe CPF e senha e autentica o usuário.",
        examples=[
            OpenApiExample(
                'Exemplo de Requisição de Login',
                value={
                    'cpf': '12345678900', # Ou '123.456.789-00' dependendo do que seu frontend envia
                    'senha': 'sua_senha_segura'
                },
                request_only=True,
                media_type='application/json',
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            auth_login(request, user)  # Session-based login
            return Response({"message": "Login realizado com sucesso!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CadastroAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=CadastroSerializer, # Informa qual serializer define o corpo da requisição
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {
                        'type': 'string', 
                        'description': 'Usuário cadastrado com sucesso!'
                    }
                }
            },
            400: {
                'description': 'Credenciais inválidas ou dados de requisição incorretos.'
            },
        },
        summary="Insere um novo usuário.",
        description="Este endpoint recebe CPFm, email, nome, role e senha, valida os dados e cadastra o usuário.",
        examples=[
            OpenApiExample(
                'Exemplo de Requisição de Login',
                value={
                    'cpf': '12345678900', # Ou '123.456.789-00' dependendo do que seu frontend envia
                    'email': 'usuario@email.com',
                    'nome': 'João da Silva',
                    'role': 'default ou admin',
                    'senha': 'sua_senha_segura'
                },
                request_only=True,
                media_type='application/json',
            )
        ]
    )

    def post(self, request):
        serializer = CadastroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        auth_logout(request)
        return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK)
