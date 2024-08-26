from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import ClienteUser

class ClienteUserCriarForm(UserCreationForm):
   
    perfil_imagem = forms.ImageField(
        required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ClienteUser
        fields = ('username', 'email', 'password1', 'password2', 'perfil_imagem')
        
        # Aplique a classe 'form-control' aos campos de entrada
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    # Validação customizada para a senha
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        # Verifica se a senha tem menos de 8 caracteres
        if len(password1) < 8:
            raise forms.ValidationError('Pelo menos 8 caracteres.')
        
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Pelo menos uma letra maiúscula.')
        
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Deve conter números.')
        
        if username and password1 and username.lower() in password1.lower():
            raise forms.ValidationError('Não pode ser semelhante ao nome de usuário.')
        return password1
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')  # Aqui deve ser password1, não pas
        
        if password2 != password1:
            raise forms.ValidationError('As senhas não correspondem.')
        
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            raise forms.ValidationError('O endereço de e-mail fornecido é inválido.')
        
        # Verifica se o e-mail já está em uso
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
    
        return email
class ClienteUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        
        if not user.check_password(self.cleaned_data.get('password')):
            raise forms.ValidationError(
                'Senha incorreta. Tente novamente.',
                code='password_invalid'
            )