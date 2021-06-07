import json
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from data_consig.data_flow import DataFlow
from data_consig.data_treatment.models_treatment.contrato_cartao_treatment import ContratoCartaoTreatment
from data_consig.data_treatment.models_treatment.contrato_emprestimo_treatment import ContratoEmprestimoTreatment
from data_consig.data_treatment.models_treatment.matricula_detalhada_treatment import MatriculaDetalhadaTreatment
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo, ContratoCartao


class TestDataFlowCpf(TestCase):

    def setUp(self) -> None:
        self.cpf_pesquisado = '02149518805'
        self.matriculas = ['3413354', '356324534', '65346346']

    def create_matriculas(self):
        for matricula in self.matriculas:
            Matricula.objects.create(
                cpf=self.cpf_pesquisado,
                matricula=matricula
            )

    # region CPF
    # @skip("Não quero testar")
    def test_data_match_on_db_cpf(self):
        self.create_matriculas()

        result_db_matriculas = [
            x.matricula for x in DataFlow(cpf=self.cpf_pesquisado).verify_on_db()['matriculas']
        ]
        expected_matriculas = [
            x.matricula for x in Matricula.objects.filter(cpf=self.cpf_pesquisado)
        ]
        self.assertEqual(expected_matriculas, result_db_matriculas)

    # @skip("Não quero testar")
    def test_cpf_does_not_exist(self):
        result_db = DataFlow(cpf=self.cpf_pesquisado).verify_on_db()
        self.assertEqual(result_db, {'error_msg': 'CPF não encontrado'})

    # @skip("Não quero testar")
    def test_invalid_timestamp_cpf(self):
        Matricula.objects.filter(cpf='02149518805').update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        for matricula in Matricula.objects.filter(cpf='02149518805'):
            result_timestamp = DataFlow(cpf='02149518805').verify_timestamp(matricula)
            self.assertEqual(result_timestamp, False)

    # @skip("Não quero testar")
    def test_valid_timestamp_cpf(self):
        for matricula in Matricula.objects.filter(cpf='02149518805'):
            result_timestamp = DataFlow(cpf='02149518805').verify_timestamp(matricula)
            self.assertEqual(result_timestamp, False)

    # @skip("Não quero testar")
    def test_valid_on_api(self):
        pass

    # @skip("Não quero testar")
    def test_db_commit(self):
        pass

    # endregion


class TestDataFlowMatricula(TestCase):

    def setUp(self) -> None:
        self.matricula_pesquisada = '245633525425362'
        self.matriculas = ['706240146', '356324534', '65346346']
        self.maxDiff = None

    def create_matricula_detalhada(self):
        for matricula in self.matriculas:
            Matricula.objects.create(
                cpf='02149518805',
                matricula=matricula
            )

        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        treated_data = MatriculaDetalhadaTreatment(data).treat_and_retrieve()

        treated_data['matricula_id'] = Matricula.objects.get(matricula='706240146')

        MatriculaDetalhada.objects.create(**treated_data)

        return data

    def create_contrato(self, data, matricula_detalhada, treatment_function, model):
        treated_data = treatment_function(data).treat_and_retrieve()
        for contrato_treated in treated_data:
            contrato_treated['matricula_id'] = matricula_detalhada
            model.objects.create(**contrato_treated)

    def create_contratos_table(self):
        data = self.create_matricula_detalhada()

        matricula_detalhada = MatriculaDetalhada.objects.get(matricula='706240146')

        self.create_contrato(data, matricula_detalhada, ContratoEmprestimoTreatment, ContratoEmprestimo)
        self.create_contrato(data, matricula_detalhada, ContratoCartaoTreatment, ContratoCartao)

    # region Matricula Especifica
    # @skip("Não quero testar")
    def test_data_match_on_db_matricula_does_not_exist(self):
        matriculas = ['3413354', '356324534', '65346346']
        for matricula in matriculas:
            Matricula.objects.create(
                cpf='4253225423',
                matricula=matricula
            )

        result_db = DataFlow(matricula='3413354').verify_on_db()
        self.assertEqual(result_db, {'error_msg': 'Matrícula não encontrada'})

    # @skip("Não quero testar")
    def test_data_match_on_db_matricula(self):
        self.create_contratos_table()

        information = DataFlow(matricula='706240146').verify_on_db()

        self.assertEqual(
            information['matricula_detalhada'],
            MatriculaDetalhada.objects.get(matricula='706240146')
        )

        self.assertEqual(
            information['contratos_emprestimo'].__dict__,
            ContratoEmprestimo.objects.filter(matricula='706240146').__dict__
        )

        self.assertEqual(
            information['contratos_cartao'].__dict__,
            ContratoCartao.objects.filter(matricula='706240146').__dict__
        )

    # @skip("Não quero testar")
    def test_matricula_does_not_exist(self):
        result_db = DataFlow(matricula=self.matricula_pesquisada).verify_on_db()
        self.assertEqual(result_db, {'error_msg': 'Matrícula não encontrada'})

    # @skip("Não quero testar")
    def test_invalid_timestamp_matricula(self):
        self.create_matricula_detalhada()

        MatriculaDetalhada.objects.filter(matricula='706240146').update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        result_timestamp = DataFlow(matricula='706240146').verify_timestamp(
            MatriculaDetalhada.objects.get(matricula='706240146')
        )

        self.assertEqual(result_timestamp, False)

    # @skip("Não quero testar")
    def test_valid_timestamp_matricula(self):
        self.create_matricula_detalhada()

        result_timestamp = DataFlow(matricula='706240146').verify_timestamp(
            MatriculaDetalhada.objects.get(matricula='706240146')
        )

        self.assertEqual(result_timestamp, True)

    # endregion
