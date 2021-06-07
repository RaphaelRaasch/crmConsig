from data_consig.data_treatment.data_treatment import DataTreatment
from data_consig.models import MatriculaDetalhada, UNDESIRABLE_COLUMNS


class MatriculaDetalhadaTreatment(DataTreatment):

    def __init__(self, matricula_dict: dict, real_time: bool = False) -> None:
        self.matricula_dict = matricula_dict
        # Essa variável é do tipo lista e traz todos os nomes dos campos do modelo em questão
        self.__model_keys = [
            field.attname for field in MatriculaDetalhada._meta.fields
            if field.attname not in UNDESIRABLE_COLUMNS
        ]
        self.__treated_dict = {
            self.__model_keys[31]: real_time
        }

    def get_variables(self):
        matricula = self.matricula_dict
        dados_bancarios = self.check_key_in('dadosBancarios', matricula)
        especie = self.check_key_in('especie', matricula)
        banco = self.check_key_in('banco', dados_bancarios)
        agencia = self.check_key_in('agencia', dados_bancarios)
        endereco = self.check_key_in('endereco', agencia)
        meio_pagamento = self.check_key_in('meioPagamento', dados_bancarios)
        representante_legal = self.check_key_in('possuiRepresentanteLegalProcurador', matricula)
        pensao_alimentica = self.check_key_in('pensaoAlimenticia', matricula)
        bloqueio_emprestimo = self.check_key_in('bloqueioEmprestismo', matricula)
        permite_emprestimo = self.check_key_in('beneficioPermiteEmprestimo', matricula)
        margem = self.check_key_in('margem', matricula)
        margem_calculo = self.check_key_in('baseCalculoMargemConsignavel', margem)
        margem_emprestimo = self.check_key_in('margemDisponivelEmprestimo', margem)
        quantidade_emprestimo = self.check_key_in('quantidadeEmprestimo', margem)
        possui_cartao = self.check_key_in('possuiCartao', margem)
        margem_cartao = self.check_key_in('margemDisponivelCartao', margem)
        margem_competencia = self.check_key_in('competencia', margem)
        return (
            matricula, dados_bancarios, especie, banco, agencia, endereco,
            meio_pagamento, representante_legal, pensao_alimentica, bloqueio_emprestimo,
            permite_emprestimo, margem_calculo, margem_emprestimo, margem, quantidade_emprestimo,
            possui_cartao, margem_cartao, margem_competencia
        )

    def treat_and_retrieve(self):
        self.insert_non_treated_values()
        self.insert_treated_values()
        return self.__treated_dict

    def insert_non_treated_values(self) -> None:
        matricula, dados_bancarios, especie, banco, agencia, endereco, meio_pagamento, *_ = self.get_variables()
        self.__treated_dict.update({
            # region Dados pessoais
            self.__model_keys[0]: matricula.get('cpf'),
            self.__model_keys[1]: matricula.get('nome'),
            self.__model_keys[3]: matricula.get('identidade'),
            self.__model_keys[4]: matricula.get('sexo'),
            # endregion

            # region Dados bancarios, estão inseridos dentro de um dicionário
            self.__model_keys[5]: self.check_key_in('codigo', banco),
            self.__model_keys[6]: self.check_key_in('nome', banco),
            self.__model_keys[7]: self.check_key_in('codigo', agencia),
            self.__model_keys[8]: self.check_key_in('nome', agencia),
            self.__model_keys[9]: self.check_key_in('endereco', endereco),
            self.__model_keys[10]: self.check_key_in('uf', endereco),
            self.__model_keys[12]: self.check_key_in('tipo', meio_pagamento),
            self.__model_keys[13]: self.check_key_in('numero', meio_pagamento),
            # endregion

            # region Dados de matrícula
            self.__model_keys[14]: self.check_key_in('beneficio', matricula),
            self.__model_keys[15]: self.check_key_in('situacaoBeneficio', matricula),
            self.__model_keys[16]: self.check_key_in('nit', matricula),
            self.__model_keys[17]: self.check_key_in('codigo', especie),
            self.__model_keys[18]: self.check_key_in('descricao', especie),
            # endregion
        })

    def insert_treated_values(self):
        (
            matricula, dados_bancarios, _, _, agencia, _, _, representante_legal, pensao_alimenticia,
            bloqueio_emprestimo, permite_emprestimo, margem_calculo, margem_emprestimo, margem, quantidade_emprestimo,
            possui_cartao, margem_cartao, margem_competencia
        ) = self.get_variables()

        self.__treated_dict.update({
            # region Dados pessoais
            self.__model_keys[2]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('dataNascimento', matricula)
            )),
            # endregion

            # region Dados bancarios
            self.__model_keys[11]: self.int_treatment(agencia.get('orgaoPagador')) if agencia else None,
            # endregion

            # region Dados de matricula
            self.__model_keys[19]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('dib', matricula)
            )),
            self.__model_keys[20]: self.float_treatment(
                self.check_key_in('valorBeneficio', matricula)
            ),
            self.__model_keys[21]: self.bool_treatment(representante_legal),
            self.__model_keys[22]: self.bool_treatment(pensao_alimenticia),
            self.__model_keys[23]: self.bool_treatment(bloqueio_emprestimo),
            self.__model_keys[24]: self.bool_treatment(permite_emprestimo),
            # endregion

            # region Dados de margem
            self.__model_keys[25]: self.convert_to_date(*self.date_treatment(
                margem_competencia
            )),
            self.__model_keys[26]: self.float_treatment(margem_calculo),
            self.__model_keys[27]: self.float_treatment(margem_emprestimo),
            self.__model_keys[28]: self.int_treatment(quantidade_emprestimo),
            self.__model_keys[29]: self.bool_treatment(possui_cartao),
            self.__model_keys[30]: self.float_treatment(margem_cartao),
            # endregion
        })
