from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from .models import ActiveSession
from django.contrib import messages
from django.contrib.auth import logout

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            if request.user.role == 'deafult' and 'cadastro' in request.path:
                return redirect('lista_solicitacoes')
        return self.get_response(request)
    
class LimitSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                active_session = request.user.active_session
                if active_session.session_key != request.session.session_key:
                    # Invalidar a sessão atual
                    Session.objects.filter(session_key=active_session.session_key).delete()
                    messages.warning(request, f"Devido ao tempo de inatividade, você foi desconectado. Por favor, faça login novamente!")
                    logout(response)
                    return redirect('login')
                
            except ActiveSession.DoesNotExist:
                request.user.active_session = ActiveSession.objects.create(
                    user=request.user,
                    session_key=request.session.session_key
                )
        response = self.get_response(request)

        return response