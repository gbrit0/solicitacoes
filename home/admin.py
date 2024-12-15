from django.contrib import admin
from home.models import User, Solicitacao
# Register your models here.
class ListSolicitacoes(admin.ModelAdmin):
   list_display = ("id", "solicitante", "produto", "quantidade", "data_de_necessidade", "obs")
   list_display_links = ("id", "solicitante", "produto", "quantidade", "data_de_necessidade", "obs")
   search_fields = ("id", "solicitante", "produto", "quantidade", "data_de_necessidade", "obs")
   list_per_page = 10

admin.site.register(Solicitacao, ListSolicitacoes)

class ListUsers(admin.ModelAdmin):
   list_display = ("cpf", "nome", "sobrenome", "email", "data_cadastro", "admin")
   list_display_links = ("cpf", "nome", "sobrenome", "email", "data_cadastro")
   search_fields = ("cpf", "nome", "sobrenome", "email")
   list_per_page = 10

admin.site.register(User, ListUsers)