from django.shortcuts import redirect

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            if request.user.role == 'deafult' and 'cadastro' in request.path:
                return redirect('lista_solicitacoes')
        return self.get_response(request)