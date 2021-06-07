from django.db import models


class Convenio(models.Model):

    TIPO_CHOICES = (
        ('INSS', 'INSS'),
        ('FEDERAL', 'FEDERAL'),
        ('FORCAS', 'FORCAS'),
        ('GOVERNO', 'GOVERNO'),
    )

    tipo_convenio = models.CharField(max_length=11, choices=TIPO_CHOICES)
    convenio = models.CharField(max_length=155)
    perfil = models.CharField(max_length=11)
    descricao = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)