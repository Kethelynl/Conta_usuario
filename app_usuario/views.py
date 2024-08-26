from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from .forms import ClienteUserCriarForm, ClienteUserLoginForm
from django.http import HttpResponse
# Create your views here.
def cadastro(request):
    if request.method == 'POST':
        form = ClienteUserCriarForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('login')
        
        else:
            print("Formulário inválido:", form.errors)  # Adicione isso para ver os erros
    else:
        form = ClienteUserCriarForm()
        
    return render(request, 'cadastro.html', {'form':form})

def cadastrado(request):
    return render(request, 'cadastro.html')

class ClienteUserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = ClienteUserLoginForm

    
    def form_invalid(self, form):
        # Adiciona uma mensagem de erro personalizada
        if form.non_field_errors():
            form.add_error(None, 'Nome de usuário ou senha incorretos.')
        return super().form_invalid(form)
    
@login_required
def perfil(request):
    user = request.user
    return render(request, 'perfil.html', {'user': user})