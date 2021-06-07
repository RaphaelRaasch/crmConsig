from django.db import models

from authentication.models import Empresa


class Filial(models.Model):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=155)
    alias = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
