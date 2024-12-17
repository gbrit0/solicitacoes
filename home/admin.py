from django.contrib import admin
from home.models import Solicitacao
# Register your models here.
class ListSolicitacoes(admin.ModelAdmin):
   list_display = ("id", "tipo", "solicitante", "produto", "quantidade", "data_de_necessidade", "obs")
   list_display_links = ("id", "tipo", "solicitante", "produto", "quantidade", "data_de_necessidade", "obs")
   search_fields = ("id", "tipo", "solicitante", "produto", "quantidade", "data_de_necessidade", "obs")
   list_per_page = 10

admin.site.register(Solicitacao, ListSolicitacoes)
