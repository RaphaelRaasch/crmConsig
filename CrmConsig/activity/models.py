from django.db import models

from CrmConsig.settings import DEFAULT_MAX_LENGTH, SMALL_MAX_LENGHT
from authentication.models import Usuario, Empresa
from data_consig.models import MatriculaDetalhada

status = (
    (2, 'Mudo/Inexistente'),
    (4, 'Não Existe Telefone'),
    (6, 'Não Encontrado/Engano'),
    (8, 'Não Atende - Só Chama'),
    (10, 'Não Atende - Ocupado'),
    (12, 'Não Atende - Caixa Postal/Desligado'),
    (14, 'Nenhuma Operação Disponível no Momento'),
    (16, 'Falecido'),
    (18, 'Não Deseja Receber Contato'),
    (1, 'Não Pode Atender a Ligação'),
    (20, 'Margem Insuficiente'),
    (3, 'Cliente com Possibilidade'),
    (5, 'Recado com Terceiros'),
    (22, 'Cliente Sem Interesse'),
    (7, 'Cliente vai Pensar'),
    (9, 'Agendado'),
    (11, 'Em Negociação'),
    (13, 'Aceitou a Oferta'),
    (15, 'Cliente Já Contratado'),
)


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField("Está ativo", default=True)

    class Meta:
        abstract = True


class Activity(AbstractModel):
    matricula = models.ForeignKey(MatriculaDetalhada, on_delete=models.CASCADE, null=True)
    cpf = models.CharField('CPF', max_length=SMALL_MAX_LENGHT, default='')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    phone = models.CharField('Telefone', max_length=SMALL_MAX_LENGHT)
    obs = models.CharField('Observação', max_length=DEFAULT_MAX_LENGTH, blank=True, default='')
    status = models.IntegerField('Retorno', choices=status)
    date_return = models.DateTimeField('Data de Retorno', null=True, blank=True)

    class Meta:
        verbose_name = 'Atividade'


class QueryClient(AbstractModel):
    matricula = models.ForeignKey(MatriculaDetalhada, on_delete=models.CASCADE, null=True)
    cpf = models.CharField('CPF', max_length=SMALL_MAX_LENGHT, default='')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)

    class Meta:
       verbose_name = 'Histórico Realtime'
       verbose_name_plural = 'Históricos Realtime'
