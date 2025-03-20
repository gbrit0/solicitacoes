from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.cpf_funcs import cpf_validate
from django.utils import timezone
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError(_("O CPF é obrigatório"))
        if not email:
            raise ValueError(_("O email é obrigatório"))
        
        # Normaliza o email e o CPF
        email = self.normalize_email(email)
      #   cpf = cpf.replace(".", "").replace("-", "")
        extra_fields.setdefault("is_active", True)

        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(cpf, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('default', 'Padrão')
    )

    id = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
        default=None,
        null=False  # Adicionado temporariamente apenas para migração
    )

    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        validators=[cpf_validate],
        primary_key=True
    )
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    role = models.CharField(max_length=20, choices=ROLES, default='default')
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'nome', 'role']

    class Meta:
        permissions = [
            ("ver_todas_solicitacoes", "Pode ver todas as solicitações"),  # Corrigido para usar parênteses
            ("criar_novos_usuários", "Pode criar novos usuários")
        ]

    def __str__(self):
        return f"{self.nome}"
    
    def save(self, *args, **kwargs):
        # Verifica se é uma nova instância (sem ID)
        if not self.id:
            # Gera um novo ID sequencial
            ultimo_usuario = CustomUser.objects.order_by('-id').first()
            if ultimo_usuario and ultimo_usuario.id:
                try:
                    # Tenta converter o último ID para um número e incrementar
                    ultimo_id = int(ultimo_usuario.id)
                    novo_id = str(ultimo_id + 1).zfill(6)  # Garante 6 dígitos com zeros à esquerda
                except ValueError:
                    # Caso o ID não seja numérico, comece com '000001'
                    novo_id = '000001'
            else:
                # Se não existir usuário anterior, comece com '000001'
                novo_id = '000001'
            self.id = novo_id
            
        # Remove caracteres não numéricos do CPF
        self.cpf = re.sub(r'\D', '', self.cpf)
        super().save(*args, **kwargs)
