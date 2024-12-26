from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
   def decorator(view_func):
      @wraps(view_func)
      def wrapped(request, *args, **kwargs):
         if request.user.role in allowed_roles:
            return view_func(request, *args, **kwargs)
         messages.error(request, f"Você não possui autorização para acessar esta página! Contate o administrador.")
         return redirect('lista_solicitacoes')
      return wrapped
   return decorator