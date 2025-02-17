from django.contrib import admin
from .models import Solicitacao, Produto

class SolicitacaoAdmin(admin.ModelAdmin):
   list_display = ('c1_filial', 'c1_num', 'c1_emissao', 'user')
   list_display_link = ('c1_filial', 'c1_num', 'c1_emissao', 'user')
   search_fields = ('c1_num', 'user')
   ordering = ('c1_num',)

class ProdutoAdmin(admin.ModelAdmin):
   list_display = ('c1_num', 'c1_item', 'c1_descri', 'c1_quant', 'c1_datprf', 'ctj_desc')
   list_display_link = ('c1_num', 'c1_item', 'c1_descri', 'c1_quant', 'c1_datprf', 'ctj_desc')
   search_fields = ('c1_num', 'c1_descri')
   ordering = ('c1_num',)
   

admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(Produto, ProdutoAdmin)