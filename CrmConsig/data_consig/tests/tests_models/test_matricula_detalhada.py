import json

from django.test import TestCase

from data_consig.data_treatment.models_treatment.matricula_detalhada_treatment import MatriculaDetalhadaTreatment
from data_consig.models import Matricula, MatriculaDetalhada
from data_consig.tests.api_matricula.expected_dict.matricula_detalhada import (
    EXPECTED_NB_5466201169, EXPECTED_NB_706240146
)


class TestMatriculaDetalhada(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        undesirable_columns = ['created_at', 'updated_at']
        self.__model_keys = [
            field.attname for field in MatriculaDetalhada._meta.fields
            if field.attname not in undesirable_columns
        ]

    @staticmethod
    def create_matricula_detalhada(data):
        treated_data = MatriculaDetalhadaTreatment(data).treat_and_retrieve()
        db_matricula = Matricula.objects.create(
            cpf=treated_data.get('cpf'),
            matricula=treated_data.get('matricula_id')
        )
        treated_data['matricula_id'] = db_matricula
        return MatriculaDetalhada.objects.create(**treated_data)

    def manipulate_and_create_matricula(self, data):
        matricula_detalhada = self.create_matricula_detalhada(data)
        matricula = MatriculaDetalhada.objects.get(cpf=matricula_detalhada.cpf)
        return {key: value for key, value in matricula.__dict__.items() if key in self.__model_keys}

    # @skip("Não quero testar")
    def test_create_and_get_objects_706240146(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        matricula_dict = self.manipulate_and_create_matricula(data)

        self.assertEqual(matricula_dict, EXPECTED_NB_706240146.EXPECTED_DICT_706240146)

    # @skip("Não quero testar")
    def test_create_and_get_objects_5466201169(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_5466201169.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        matricula_dict = self.manipulate_and_create_matricula(data)

        self.assertEqual(matricula_dict, EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169)

    # @skip("Não quero testar")
    def test_create_and_get_objects_5466201169_error(self):
        with open('data_consig/tests/api_matricula/test_json/NB_5466201169_error.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        matricula_dict = self.manipulate_and_create_matricula(data)

        self.assertEqual(matricula_dict, EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169)

    def test_delete_matricula_drops_matricula_detalhada(self):
        with open('data_consig/tests/api_matricula/test_json/NB_5466201169_error.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.manipulate_and_create_matricula(data)

        self.assertEqual(
            str(MatriculaDetalhada.objects.get(matricula='5466201169').matricula),
            '5466201169'
        )

        Matricula.objects.get(matricula='5466201169').delete()
        self.assertRaises(
            Matricula.DoesNotExist,
            Matricula.objects.get,
            matricula='5466201169'
        )
        self.assertRaises(
            MatriculaDetalhada.DoesNotExist,
            MatriculaDetalhada.objects.get,
            matricula='5466201169'
        )
