from django.db import models


class Status(models.Model):

    PERFIL_CHOICES = (
        (' Comercial',' Comercial'),
        (' Esteira',' Esteira'),
        (' Telefone',' Telefone')
    )

    status = models.CharField(max_length=50)
    perfil = models.CharField(max_length=12, choices=PERFIL_CHOICES)
    descricao = models.CharField(max_length=155)

    def __str__(self):
        return self.status