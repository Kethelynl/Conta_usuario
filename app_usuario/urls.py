from django.urls import path
from . import views
urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('cadastro/', views.cadastrado, name='cadastrado'),
    path('login/', views.ClienteUserLoginView.as_view(), name='login'),
    path('perfil/', views.perfil, name='perfil'),
]
