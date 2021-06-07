from data_consig.data_treatment.data_treatment import DataTreatment
from data_consig.models import ContratoCartao, UNDESIRABLE_COLUMNS


class ContratoCartaoTreatment(DataTreatment):
    def __init__(self, matricula_dict_list: dict) -> None:
        self.matricula_dict = matricula_dict_list
        self.__model_keys = [
            field.attname for field in ContratoCartao._meta.fields
            if field.attname not in UNDESIRABLE_COLUMNS
        ]

        self.contratos_cartao = self.check_key_in('contratosCartao', self.matricula_dict)

        self.__treated_list = []

    def treat_and_retrieve(self):
        self.verify_input_type()
        return self.__treated_list

    def verify_input_type(self):
        if type(self.contratos_cartao) == dict():
            self.update_treated_dict(self.matricula_dict)
        elif type(self.contratos_cartao) == list:
            for contrato in self.contratos_cartao:
                self.update_treated_dict(contrato)

    def get_variables(self, contratos_cartao: dict) -> tuple:
        codigo_cartao = self.check_key_in('contrato', contratos_cartao)
        tipo_cartao = self.check_key_in('tipoEmprestimo', contratos_cartao)
        banco = self.check_key_in('banco', contratos_cartao)
        return (
            contratos_cartao, codigo_cartao, tipo_cartao, banco
        )

    def update_treated_dict(self, contratos_cartao: dict) -> None:
        (
            contratos_cartao, codigo_cartao, tipo_cartao, banco
        ) = self.get_variables(contratos_cartao)

        treated_dict = {
            # region Dados não tratados
            self.__model_keys[0]: self.check_key_in('contrato', contratos_cartao),
            self.__model_keys[1]: self.check_key_in('beneficio', self.matricula_dict),
            self.__model_keys[2]: self.check_key_in('codigo', tipo_cartao),
            self.__model_keys[3]: self.check_key_in('descricao', tipo_cartao),
            self.__model_keys[4]: self.check_key_in('codigo', banco),
            self.__model_keys[5]: self.check_key_in('nome', banco),
            self.__model_keys[8]: self.check_key_in('situacao', contratos_cartao),
            # endregion

            # region Dados tratados
            self.__model_keys[6]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('dataInicioContrato', contratos_cartao)
            )),
            self.__model_keys[7]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('dataInclusao', contratos_cartao)
            )),
            self.__model_keys[9]: self.bool_treatment(
                self.check_key_in('excluidoAps', contratos_cartao)
            ),
            self.__model_keys[10]: self.bool_treatment(
                self.check_key_in('excluidoBanco', contratos_cartao)
            ),
            self.__model_keys[11]: self.float_treatment(
                self.check_key_in('limiteCartao', contratos_cartao)
            ),
            self.__model_keys[12]: self.float_treatment(
                self.check_key_in('valorReservado', contratos_cartao)
            ),
            # endregion
        }
        self.__treated_list.append(treated_dict)
