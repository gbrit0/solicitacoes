class ProtheusRouter:
   """Router para operações do model SC1 para o banco do Protheus"""

   def db_for_read(self, model, **hints):
      if model._meta.app_label == 'home' and model._meta.model_name == 'solicitacaocompra':
         return 'protheus'
      return None
   
   def db_for_write(self, model, **hints):
      if model._meta.app_label == 'home' and model._meta.model_name == 'solicitacaocompra':
         return 'protheus'
      return None