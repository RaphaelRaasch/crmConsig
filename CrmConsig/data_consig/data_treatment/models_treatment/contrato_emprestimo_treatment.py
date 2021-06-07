from data_consig.data_treatment.data_treatment import DataTreatment
from data_consig.models import ContratoEmprestimo, UNDESIRABLE_COLUMNS


class ContratoEmprestimoTreatment(DataTreatment):

    def __init__(self, matricula_dict_list: dict) -> None:
        self.matricula_dict = matricula_dict_list
        self.__model_keys = [
            field.attname for field in ContratoEmprestimo._meta.fields
            if field.attname not in UNDESIRABLE_COLUMNS
        ]
        self.contratos_emprestimo = self.check_key_in('contratosEmprestimo', self.matricula_dict)

        self.__treated_list = []

    def treat_and_retrieve(self):
        self.verify_input_type()
        return self.__treated_list

    def verify_input_type(self):
        if type(self.contratos_emprestimo) == dict:
            self.update_treated_dict(self.matricula_dict)
        elif type(self.contratos_emprestimo) == list:
            for contrato in self.contratos_emprestimo:
                self.update_treated_dict(contrato)

    def get_variables(self, contratos_emprestimo: dict) -> tuple:
        codigo_emprestimo = self.check_key_in('contrato', contratos_emprestimo)
        tipo_emprestimo = self.check_key_in('tipoEmprestimo', contratos_emprestimo)
        banco = self.check_key_in('banco', contratos_emprestimo)
        return (
            contratos_emprestimo, codigo_emprestimo, tipo_emprestimo, banco
        )

    def update_treated_dict(self, contratos_emprestimo: dict) -> None:
        (
            contratos_emprestimo, codigo_emprestimo, tipo_emprestimo, banco
        ) = self.get_variables(contratos_emprestimo)

        treated_dict = {
            # region Dados não tratados
            self.__model_keys[0]: self.check_key_in('contrato', contratos_emprestimo),
            self.__model_keys[1]: self.check_key_in('beneficio', self.matricula_dict),
            self.__model_keys[2]: self.check_key_in('codigo', tipo_emprestimo),
            self.__model_keys[3]: self.check_key_in('descricao', tipo_emprestimo),
            self.__model_keys[4]: self.check_key_in('codigo', banco),
            self.__model_keys[5]: self.check_key_in('nome', banco),
            self.__model_keys[10]: self.check_key_in('situacao', contratos_emprestimo),
            # endregion

            # region Dados tratados
            self.__model_keys[6]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('dataInicioContrato', contratos_emprestimo)
            )),
            self.__model_keys[7]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('competenciaInicioDesconto', contratos_emprestimo)
            )),
            self.__model_keys[8]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('competenciaFimDesconto', contratos_emprestimo)
            )),
            self.__model_keys[9]: self.convert_to_date(*self.date_treatment(
                self.check_key_in('dataInclusao', contratos_emprestimo)
            )),
            self.__model_keys[11]: self.bool_treatment(
                self.check_key_in('excluidoAps', contratos_emprestimo)
            ),
            self.__model_keys[12]: self.bool_treatment(
                self.check_key_in('excluidoBanco', contratos_emprestimo)
            ),
            self.__model_keys[13]: self.float_treatment(
                self.check_key_in('valorEmprestado', contratos_emprestimo)
            ),
            self.__model_keys[14]: self.float_treatment(
                self.check_key_in('valorParcela', contratos_emprestimo)
            ),
            self.__model_keys[15]: self.int_treatment(
                self.check_key_in('quantidadeParcelas', contratos_emprestimo)
            ),
            self.__model_keys[16]: self.int_treatment(
                self.check_key_in('quantidadeParcelasEmAberto', contratos_emprestimo)
            ),
            self.__model_keys[17]: self.float_treatment(
                self.check_key_in('saldoQuitacao', contratos_emprestimo)
            ),
            self.__model_keys[18]: self.float_treatment(
                self.check_key_in('taxa', contratos_emprestimo)
            ),
            # endregion
        }
        self.__treated_list.append(treated_dict)
