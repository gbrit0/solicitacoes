from django.shortcuts import render, redirect
from django.forms import ModelForm
from solicitacoes.models import Produto, Solicitacao
from django.forms import inlineformset_factory
from django.utils import timezone
import pyodbc, os
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.contrib.auth.decorators import login_required

from solicitacoes.forms import ProdutosForm, SolicitacaoForm


class SolicitacaoInline():
   form_class = SolicitacaoForm
   model = Solicitacao
   template = "solicitacoes/criar_solicitacao.html"

   def form_valid(self, form):
      named_formsets = self.get_named_formsets()
      if not all((x.is_valid() for x in named_formsets.values())):
         return self.render_to_response(self.get_context_data(form=form))
      
      self.object = form.save()

      for name, formset in named_formsets.items():
         formset_save_func = getattr(self, 'formset_{0}_valid'.format(name))
         if formset_save_func is not None:
            formset_save_func(formset)
         else:
            formset.save()
      return redirect('products:list_products')
   
   def formset_products_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        products = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for product in products:
            product.c1_num = self.object
            product.save()

# class SolicitacaoCreate(SolicitacaoInline, CreateView):
#    def get_context_data(self, **kwargs):
#       ctx = super(SolicitacaoCreate, self).get_context_data(**kwargs)
#       ctx['named_formsets'] = self.get_named_formsets()
#       return ctx
   
#    def get_named_formsets(self):
#       if self.request.method == 'GET':
#          return {
#             'produtos': ProdutosFormSet
#          }


@login_required(login_url='login')
def criar_solicitacao(request):
   ProductFormset = inlineformset_factory(
      Solicitacao,
      Produto,
      form=ProdutosForm,
      fields=('c1_produto', 'c1_quant'),
      extra=1,
      can_delete=True
   )
    
   if request.method == 'POST':
      solicitacao_form = SolicitacaoForm(request.POST)
      
      formset = ProductFormset(request.POST)
      
      if solicitacao_form.is_valid():
         # Cria a solicitação sem salvar ainda
         solicitacao = solicitacao_form.save(commit=False)
         
         # Preenche os campos automáticos
         solicitacao.c1_filial = '0101'
         solicitacao.c1_user = '000000'
         solicitacao.c1_emissao = timezone.now()
         solicitacao.user = request.user
         
         connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"

         with pyodbc.connect(connectionString) as conexao:
            with conexao.cursor() as cursor:
               cursor.execute("""SELECT 
                                    MAX(CONVERT(INT, C1_NUM))
                                 FROM SC1010
                                 WHERE TRIM(C1_NUM) NOT LIKE '%G%' 
                                 AND C1_NUM <> '""'
                              """)
               ultimo_num = cursor.fetchall()
         if ultimo_num:
            proximo_num = str(int(ultimo_num[0][0]) + 1).zfill(6)
         else:
            proximo_num = '000001'
         
         

         solicitacao.c1_num = proximo_num
         
         solicitacao.save()
         
         # Agora trata o formset dos produtos
         formset = ProductFormset(request.POST, instance=solicitacao)

         
         if formset.is_valid():
            instances = formset.save(commit=False)
            connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"

            with pyodbc.connect(connectionString) as conexao:
               with conexao.cursor() as cursor:
                  for num, instance in enumerate(instances):
                     instance.c1_item = f"{num+1:04d}"
                     cursor.execute(f"select MAX(B1_DESC) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                     instance.c1_descri = cursor.fetchall()[0][0]
                     cursor.execute(f"select MAX(B1_UM) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                     instance.c1_um =  cursor.fetchall()[0][0]
                     cursor.execute(f"select MAX(B1_LOCPAD) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                     instance.c1_local =  cursor.fetchall()[0][0]
                     instance.save()

                     produto = str(instance.c1_descri).replace("\n", " ").replace("\r", " ")
                     insert = f"""INSERT INTO SC1010
                                 (C1_FILIAL, C1_NUM, C1_ITEM, C1_DESCRI, C1_CC, C1_PRODUTO, 
                                 C1_LOCAL, C1_QUANT, C1_EMISSAO, C1_DATPRF, C1_SOLICIT, C1_OBS, R_E_C_N_O_)
                                 VALUES ('{solicitacao.c1_filial}', 
                                          '{solicitacao.c1_num}', 
                                          '{instance.c1_item}', 
                                          '{produto}', 
                                          '{solicitacao.c1_cc}', 
                                          '{instance.c1_produto}', 
                                          '{instance.c1_local}', 
                                          '{instance.c1_quant}', 
                                          '{str(solicitacao.c1_emissao).replace("-", "")[:8]}', 
                                          '{str(solicitacao.c1_datprf).replace("-", "")}', 
                                          '{solicitacao.c1_solicit}', 
                                          '{solicitacao.c1_obs}', 
                                          '{instance.r_e_c_n_o}')"""
                     print(instance)
                     cursor.execute(insert)
                     conexao.commit()
               
            return redirect('lista_solicitacoes')
   else:
      solicitacao_form = SolicitacaoForm()
      formset = ProductFormset()
   
   context = {
      'solicitacao_form': solicitacao_form,
      'formset': formset
   }
   
   return render(request, 'solicitacoes/criar_solicitacao.html', context)

