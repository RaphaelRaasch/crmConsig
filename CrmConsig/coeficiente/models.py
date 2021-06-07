from django.db import models
from bancos.models import Banco
from produto.models import Produto


class Coeficiente(models.Model):
    dia = models.SmallIntegerField(blank=True, null=True)
    id_banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    tabela = models.CharField(max_length=255, blank=True, null=True)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    coeficiente = models.CharField(max_length=20, blank=True, null=True)
    comissao = models.CharField(max_length=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

