from django.db import models

from CrmConsig.settings import DEFAULT_MAX_LENGTH

UNDESIRABLE_COLUMNS = ['created_at', 'updated_at', 'is_active']


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField("Está ativo", default=True)

    class Meta:
        abstract = True


class Matricula(AbstractModel):
    cpf = models.CharField("CPF", max_length=DEFAULT_MAX_LENGTH)
    matricula = models.CharField("Matrícula", max_length=DEFAULT_MAX_LENGTH, unique=True, primary_key=True)
    inserted_by_cpf_api = models.BooleanField("Inserido por API de CPF", default=False)

    # descricao = models.CharField()

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        return self.matricula


class MatriculaDetalhada(AbstractModel):
    # region Dados pessoais
    cpf = models.CharField("CPF", max_length=DEFAULT_MAX_LENGTH, null=True)  # 0
    nome = models.CharField("Nome", max_length=DEFAULT_MAX_LENGTH, null=True)  # 1
    dt_nascimento = models.DateField("Data Nascimento", null=True)  # 2
    identidade = models.CharField("Numero Identidade", max_length=DEFAULT_MAX_LENGTH, null=True)  # 3
    genero = models.CharField("Genero", max_length=DEFAULT_MAX_LENGTH, null=True)  # 4
    # endregion

    # region Dados bancarios
    codigo_banco = models.CharField("Código Banco", max_length=DEFAULT_MAX_LENGTH, null=True)  # 5
    nome_banco = models.CharField("Nome Banco", max_length=DEFAULT_MAX_LENGTH, null=True)  # 6
    codigo_agencia = models.CharField("Codigo Agencia", max_length=DEFAULT_MAX_LENGTH, null=True)  # 7
    nome_agencia = models.CharField("Nome Agencia", max_length=DEFAULT_MAX_LENGTH, null=True)  # 8
    endereco_agencia = models.CharField("Endereco Agencia", max_length=DEFAULT_MAX_LENGTH, null=True)  # 9
    uf_agencia = models.CharField("UF Agencia", max_length=DEFAULT_MAX_LENGTH, null=True)  # 10
    orgao_pagador = models.IntegerField("Orgao Pagador", null=True)  # 11
    tipo_pagamento = models.CharField("Tipo Pagamento", max_length=DEFAULT_MAX_LENGTH, null=True)  # 12
    numero_pagamento = models.CharField("Numero Pagamento", max_length=DEFAULT_MAX_LENGTH, null=True)  # 13
    # endregion

    # region Dados da matricula
    matricula = models.OneToOneField(Matricula, primary_key=True, on_delete=models.CASCADE)  # 14
    situacao = models.CharField("Situacao Matricula", max_length=DEFAULT_MAX_LENGTH, null=True)  # 15
    nit = models.CharField("NIT", max_length=DEFAULT_MAX_LENGTH, null=True)  # 16
    codigo_matricula = models.CharField("Codigo Matricula", max_length=DEFAULT_MAX_LENGTH, null=True)  # 17
    descricao_matricula = models.CharField("Descricao Matricula", max_length=DEFAULT_MAX_LENGTH, null=True)  # 18
    dib = models.DateField("DIB", null=True)  # 19
    valor_matricula = models.FloatField("Valor Matricula", null=True)  # 20
    representante_legal = models.BooleanField("Representante legal", null=True)  # 21
    pensao_alimenticia = models.BooleanField("Pensao Alimenticia", null=True)  # 22
    bloqueio_emprestimo = models.BooleanField("Bloqueio Emprestimo", null=True)  # 23
    permite_emprestimo = models.BooleanField("Permite Emprestimo", null=True)  # 24
    # endregion

    # region Dados da margem
    competencia = models.DateField("Competencia", null=True)  # 25
    margem_consignavel = models.FloatField("Margem Consignavel", null=True)  # 26
    margem_emprestimo = models.FloatField("Margem Emprestimo", null=True)  # 27
    quantidade_emprestimo = models.IntegerField("Quantidade Emprestimo", null=True)  # 28
    possui_cartao = models.BooleanField("Possui Cartao", null=True)  # 29
    margem_cartao = models.FloatField("Margem Cartao", null=True)  # 30
    # endregion

    # region Real Time
    real_time = models.BooleanField("Real Time", default=False)  # 31

    class Meta:
        verbose_name = 'Matrícula Detalhada'
        verbose_name_plural = 'Matrículas Detalhadas'

    def __str__(self):
        return str(self.matricula)


class ContratoEmprestimo(AbstractModel):
    contrato = models.CharField("Numero Contrato", max_length=DEFAULT_MAX_LENGTH, unique=True, primary_key=True)  # 0
    matricula = models.ForeignKey(MatriculaDetalhada, on_delete=models.CASCADE)  # 1
    codigo_emprestimo = models.CharField("Codigo Emprestimo", max_length=DEFAULT_MAX_LENGTH, null=True)  # 2
    descricao_emprestimo = models.CharField("Descricao Emprestimo", max_length=DEFAULT_MAX_LENGTH, null=True)  # 3
    codigo_banco = models.CharField("Codigo Banco", max_length=DEFAULT_MAX_LENGTH, null=True)  # 4
    nome_banco = models.CharField("Nome Banco", max_length=DEFAULT_MAX_LENGTH, null=True)  # 5
    data_inicio = models.DateField("Data Inicio Contrato", null=True)  # 6
    competencia_inicio_desconto = models.DateField("Competencia Inicio Desconto", null=True)  # 7
    competencia_fim_desconto = models.DateField("Competencia Fim Desconto", null=True)  # 8
    data_inclusao = models.DateField("Data Inclusao", null=True)  # 9
    situacao = models.CharField("Situacao Contrato", max_length=DEFAULT_MAX_LENGTH, null=True)  # 10
    excluido_aps = models.BooleanField("Excluido APS", null=True)  # 11
    excluido_banco = models.BooleanField("Excluido Banco", null=True)  # 12
    valor_emprestimo = models.FloatField("Valor Emprestimo", null=True)  # 13
    valor_parcela = models.FloatField("Valor Parcela", null=True)  # 14
    quantidade_parcelas = models.IntegerField("Quantidade Parcelas", null=True)  # 15
    parcelas_aberto = models.IntegerField("Parcelas em Aberto", null=True)  # 16
    saldo = models.FloatField("Saldo para Quitação", null=True)  # 17
    taxa = models.FloatField("Taxa", null=True)  # 18

    class Meta:
        verbose_name = "Contrato de Empréstimo "
        verbose_name_plural = "Contratos de Empréstimos"

    def __str__(self):
        return f'Contrato:{self.contrato} / Valor Empréstimo: {self.valor_emprestimo}'


class ContratoCartao(AbstractModel):
    contrato = models.CharField("Numero Contrato", max_length=DEFAULT_MAX_LENGTH, unique=True, primary_key=True)  # 0
    matricula = models.ForeignKey(MatriculaDetalhada, on_delete=models.CASCADE, null=True)  # 1
    codigo_cartao = models.CharField("Codigo Cartao", max_length=DEFAULT_MAX_LENGTH, null=True)  # 2
    descricao_cartao = models.CharField("Descricao Cartao", max_length=DEFAULT_MAX_LENGTH, null=True)  # 3
    codigo_banco = models.CharField("Codigo Banco", max_length=DEFAULT_MAX_LENGTH, null=True)  # 4
    nome_banco = models.CharField("Nome Banco", max_length=DEFAULT_MAX_LENGTH, null=True)  # 5
    inicio_contrato = models.DateField("Inicio Contrato", null=True)  # 6
    inclusao_contrato = models.DateField("Inclusao Contrato", null=True)  # 7
    situacao = models.CharField("Situacao Contrato", max_length=DEFAULT_MAX_LENGTH, null=True)  # 8
    excluido_aps = models.BooleanField("Excluido APS", null=True)  # 9
    excluido_banco = models.BooleanField("Excluido Banco", null=True)  # 10
    limite_cartao = models.FloatField("Limite Cartao", null=True)  # 11
    valor_reservado = models.FloatField("Valor Reservado", null=True)  # 12

    class Meta:
        verbose_name = "Contrato de Cartão"
        verbose_name_plural = "Contratos de Cartões"

    def __str__(self):
        return f'Contrato:{self.contrato}'
