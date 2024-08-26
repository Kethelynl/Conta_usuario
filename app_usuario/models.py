from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ClienteUser(AbstractUser):
    perfil_imagem = models.ImageField(upload_to='perfil/', null=True, blank=True)
    