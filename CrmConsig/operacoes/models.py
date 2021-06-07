from django.db import models

from convenio.models import Convenio
from produto.models import Produto
from bancos.models import Banco
from coeficiente.models import Coeficiente
from data_consig.models import Matricula
from authentication.models import Usuario
from status.models import Status


class Operacoes(models.Model):
    id_convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    id_banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    id_banco_sacado = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='banco_sacado')
    id_coeficiente = models.ForeignKey(Coeficiente, on_delete=models.CASCADE)
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor_bruto = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    valor_liquido = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    saldo_devedor = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    informacao = models.CharField(max_length=200, blank=True, null=True)
    previsao_saldo = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)





"""
  `id_status` int(11) NOT NULL,
  `informacao` varchar(200) DEFAULT NULL,
  `previsao_saldo` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `update_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
"""