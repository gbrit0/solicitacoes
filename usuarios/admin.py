from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Campos que serão exibidos no admin
    list_display = ('cpf', 'email', 'nome', 'is_staff', 'is_active')
    search_fields = ('cpf', 'email', 'nome')
    ordering = ('nome',)

    # Configurações dos formulários de adição e edição
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações pessoais', {'fields': ('nome', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'email', 'nome', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

# Registra o modelo e o admin personalizado
admin.site.register(CustomUser, CustomUserAdmin)
