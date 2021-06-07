from django.db import models


class Banco(models.Model):
    nome = models.CharField(max_length=155)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=155, blank=True, null=True)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
