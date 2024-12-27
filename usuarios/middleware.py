from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime, timedelta
from django.contrib import auth

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            if request.user.role == 'deafult' and 'cadastro' in request.path:
                return redirect('lista_solicitacoes')
        return self.get_response(request)




class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        if not hasattr(request, 'session'):
            return

        session_expiry = request.session.get('session_expiry', None)
        if session_expiry:
            now = datetime.now().timestamp()
            if now > session_expiry:
                timeout_message = True
                auth.logout(request)  # Fazer logout apropriadamente
                request.session['timeout_message'] = timeout_message  # Definir após o logout
                return redirect('login')

        request.session['session_expiry'] = (datetime.now() + timedelta(seconds=15 * 60)).timestamp()

