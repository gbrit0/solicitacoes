from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Campos que serão exibidos no admin
    list_display = ('cpf', 'email', 'nome', 'role')
    list_display_links = ('cpf', 'email', 'nome')
    search_fields = ('cpf', 'email', 'nome')
    ordering = ('nome',)

    # Configurações dos formulários de adição e edição
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações pessoais', {'fields': ('nome', 'email')}),
        ('Permissões', {'fields': ('role')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'email', 'nome', 'password1', 'password2', 'role')}
        ),
    )

# Registra o modelo e o admin personalizado
admin.site.register(CustomUser, CustomUserAdmin)
