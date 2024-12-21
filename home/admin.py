from django.contrib import admin
from home.models import Solicitacao
# Register your models here.
class ListSolicitacoes(admin.ModelAdmin):
   list_display = ("c1_filial", "c1_num", "c1_cc", "c1_item", "c1_produto", "c1_descri", "c1_local", "c1_quant", "c1_datprf", "c1_user", "c1_emissao")
   list_display_links = ("c1_filial", "c1_num", "c1_cc", "c1_item", "c1_produto", "c1_descri", "c1_local", "c1_quant", "c1_datprf", "c1_user", "c1_emissao")
   search_fields = ("c1_filial", "c1_num", "c1_cc", "c1_item", "c1_produto", "c1_descri", "c1_local", "c1_quant", "c1_datprf", "c1_user", "c1_emissao")
   list_per_page = 10

admin.site.register(Solicitacao, ListSolicitacoes)
