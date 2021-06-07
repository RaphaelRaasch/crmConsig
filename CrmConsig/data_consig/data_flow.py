import datetime
import json

from django.db import IntegrityError
from django.utils import timezone

from activity.models import QueryClient
from authentication.models import Usuario
from data_consig.consult_apis import ConsultAPI
from status.models import Status
from data_consig.data_treatment.models_treatment.contrato_cartao_treatment import ContratoCartaoTreatment
from data_consig.data_treatment.models_treatment.contrato_emprestimo_treatment import ContratoEmprestimoTreatment
from data_consig.data_treatment.models_treatment.matricula_detalhada_treatment import MatriculaDetalhadaTreatment
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo, ContratoCartao


class DataFlow:

    def __init__(self, cpf=None, matricula=None, real_time=False, user=False):
        self.cpf = cpf
        self.matricula = matricula
        self.real_time = real_time
        self.matricula_error = {'error_msg': 'Matrícula não encontrada'}
        self.cpf_error = {'error_msg': 'CPF não encontrado'}
        self.api_error = {'error_msg': 'Ops... Verifique o valor digitado ou tente novamente mais tarde!'}
        self.user = user

    def inserted_by_cpf_api(self, db_result):
        if self.cpf:
            return len(list(filter(lambda x: x.inserted_by_cpf_api, db_result.get('matriculas', []))))
        elif self.matricula:
            return True

    def get_information(self, resultado=False):
        """
        A função get_cpf verifica a existencia do dado no banco de dados, valida os time
        stamps de cada matricula e retorna uma lista de matriculas atualizadas.
        :return: lista de objetos de Matricula.
        """
        db_result = self.verify_on_db()
        if 'error_msg' not in db_result and not self.is_updated(db_result):
            if self.inserted_by_cpf_api(db_result) and self.is_valid_timestamp(db_result):
                return db_result
        return self.get_api_and_drop_insert(db_result, resultado=resultado)

    def is_valid_timestamp(self, db_result):
        if 'matriculas' in db_result:
            db_result = db_result['matriculas']
            timestamp_length = list(filter(lambda x: self.verify_timestamp(x), db_result))
            if len(timestamp_length) == len(db_result):
                return True
            return False
        return self.verify_timestamp(db_result['matricula_detalhada'])

    def is_updated(self, db_result):
        if db_result.get('matricula_detalhada') and self.real_time:
            today = timezone.now()
            matricula = db_result.get('matricula_detalhada')
            updated = today - matricula.updated_at
            if updated.days == 0:
                return False
            else:
                user = Usuario.objects.filter(user_id=self.user).first()
                QueryClient.objects.create(matricula_id=matricula.pk,
                                           user_id=user.pk,
                                           cpf=matricula.cpf
                                           )
                return True
        else:
            return self.real_time

    def verify_on_db(self):
        if self.cpf:
            matriculas = Matricula.objects.filter(cpf=self.cpf)
            if matriculas:
                return {'matriculas': matriculas}
            return self.cpf_error
        try:
            return {
                'matricula_detalhada': MatriculaDetalhada.objects.get(matricula=self.matricula),
                'contratos_emprestimo': ContratoEmprestimo.objects.filter(matricula=self.matricula),
                'contratos_cartao': ContratoCartao.objects.filter(matricula=self.matricula),
            }
        except MatriculaDetalhada.DoesNotExist:
            return self.matricula_error

    @classmethod
    def verify_timestamp(cls, db_object):
        if db_object:
            today = datetime.datetime.now()
            this_year, this_month = today.year, today.month

            # Dia 25 do mês passado
            last_month_date = datetime.datetime(this_year, this_month - 1, 25)

            # Data de atualização no banco de dados convertido para datetime
            updated_at = db_object.updated_at
            db_year, db_month, db_day = updated_at.year, updated_at.month, updated_at.day
            if (last_month_date - datetime.datetime(db_year, db_month, db_day)).days >= 1:
                return False
            return True

    def get_api_and_drop_insert(self, db_result, resultado=False):
        if self.cpf:
            return self.consult_and_return_from_cpf_database(db_result, resultado=resultado)
        elif self.matricula:
            return self.consult_and_return_from_matricula_detalhada_database(db_result, resultado=resultado)

    @staticmethod
    def deactivate_activate(model, updated_values: dict, active, searched_on_api=False):
        my_model = model.objects.get(**updated_values)
        my_model.is_active = active
        if searched_on_api:
            my_model.inserted_by_cpf_api = searched_on_api
        my_model.save()

    def consult_and_return_from_cpf_database(self, db_result, resultado=False):
        if resultado and isinstance(resultado, dict):
            status_code = resultado.get('status_code')
        else:
            resultado_api = ConsultAPI().cpf(self.cpf)
            if resultado_api:
                resultado = json.loads(resultado_api.text)
                status_code = resultado_api.status_code
            else:
                return self.api_error

        if status_code == 200:
            resultados_beneficios = resultado.get('beneficios')
            cpf = resultado.get('cpf')
            if resultados_beneficios:
                matriculas_api = [
                    matricula.get('beneficio')
                    for matricula in resultados_beneficios if matricula.get('beneficio')
                ]
            else:
                matriculas_api = []
            if 'error_msg' not in db_result:
                matriculas_db = [i.matricula for i in db_result.get('matriculas', [])]

                # Inativação de objetos não desejáveis
                inactivate_from_db = list(filter(lambda x: x not in matriculas_api, matriculas_db))
                for inactive_matricula in inactivate_from_db:
                    self.deactivate_activate(
                        Matricula, {'matricula': inactive_matricula}, active=False, searched_on_api=True
                    )

                # Atualização dos objetos para ativo
                update_db = list(filter(lambda x: x in matriculas_api, matriculas_db))
                for updated_matricula in update_db:
                    self.deactivate_activate(
                        Matricula, {'matricula': updated_matricula}, active=True, searched_on_api=True
                    )

                # Insert de objetos desejáveis
                insert_in_db = list(filter(lambda x: x not in matriculas_db, matriculas_api))
                for insert_matricula in insert_in_db:
                    Matricula.objects.create(
                        cpf=cpf,
                        matricula=insert_matricula,
                        inserted_by_cpf_api=True
                    )
                return {'matriculas': Matricula.objects.filter(cpf=cpf, is_active=True)}
            elif matriculas_api:
                for matricula in matriculas_api:
                    Matricula.objects.create(cpf=cpf, matricula=matricula)
                return {'matriculas': Matricula.objects.filter(cpf=cpf, is_active=True)}
        elif (status_code == 404 or status_code == 400) and db_result:
            Matricula.objects.filter(cpf=self.cpf).update(is_active=False, updated_at=timezone.now())
        return self.cpf_error

    def consult_and_return_from_matricula_detalhada_database(self, db_result, resultado=False):
        if resultado and isinstance(resultado, dict):
            status_code = resultado.get('status_code')
        else:
            resultado_api = ConsultAPI().matricula(self.matricula, real_time=self.real_time)
            if resultado_api:
                resultado = json.loads(resultado_api.text)
                status_code = resultado_api.status_code
            else:
                return self.api_error

        if status_code == 200:
            matricula = resultado.get('beneficio')
            if not matricula:
                self.deactivate_activate(MatriculaDetalhada, {'matricula': matricula}, False)
                self.deactivate_activate(Matricula, {'matricula': matricula}, False)

            elif db_result and db_result.get('matricula_detalhada'):
                treated_matricula_detalhada = MatriculaDetalhadaTreatment(
                    resultado, self.real_time
                ).treat_and_retrieve()
                treated_matricula_detalhada['updated_at'] = timezone.now()
                MatriculaDetalhada.objects.filter(matricula=matricula).update(**treated_matricula_detalhada)

                change_contratos = [
                    (ContratoEmprestimo, ContratoEmprestimoTreatment, resultado, 'contratosEmprestimo'),
                    (ContratoCartao, ContratoCartaoTreatment, resultado, 'contratosCartao')
                ]
                for model, treatment_function, resultado, key in change_contratos:
                    self.update_contratos(model, treatment_function, resultado, key)

            elif matricula:
                self.create_matricula_and_contratos_table(
                    cpf=resultado.get('cpf'),
                    matricula=matricula,
                    data=resultado,
                    real_time=self.real_time
                )
            matricula_detalhada = MatriculaDetalhada.objects.get(matricula=matricula)
            if matricula_detalhada.is_active:
                return {
                    'matricula_detalhada': matricula_detalhada,
                    'contratos_emprestimo': ContratoEmprestimo.objects.filter(matricula=matricula, is_active=True),
                    'contratos_cartao': ContratoCartao.objects.filter(matricula=matricula, is_active=True),
                    'status': Status.objects.all()
                }
        elif (status_code == 404 or status_code == 400) and db_result:
            Matricula.objects.filter(matricula=self.matricula).update(is_active=False, updated_at=timezone.now())
        return self.matricula_error

    def update_contratos(self, model, treatment_function, resultado, key):
        if key in resultado:
            contratos_api = [
                contrato['contrato'] for contrato in resultado[key] if 'contrato' in contrato
            ]
            contratos = model.objects.filter(matricula=resultado['beneficio'])
            contratos_db = [
                contrato.contrato for contrato in contratos
            ]
            treated_contratos = treatment_function(resultado).treat_and_retrieve()

            # Inativação de objetos não desejáveis
            inactivate_from_db = list(filter(lambda x: x not in contratos_api, contratos_db))
            for contrato in inactivate_from_db:
                model.objects.filter(contrato=contrato).update(is_active=False, updated_at=timezone.now())

            # Ativação de objetos desejáveis
            activate_from_db = list(filter(lambda x: x in contratos_api, contratos_db))
            for contrato in activate_from_db:
                treated_contrato = list(filter(
                    lambda value: value.get('contrato') == contrato, treated_contratos
                ))[0]
                treated_contrato['is_active'] = True
                treated_contrato['updated_at'] = timezone.now()
                model.objects.filter(contrato=contrato).update(**treated_contrato)

            # Criação de objetos não existentes no banco de dados
            insert_from_db = list(filter(lambda x: x not in contratos_db, contratos_api))
            for contrato in insert_from_db:
                treated_contrato = list(filter(
                    lambda value: value.get('contrato') == contrato, treated_contratos
                ))[0]
                treated_contrato['is_active'] = True
                model.objects.create(**treated_contrato)
        else:
            model.objects.filter(matricula=resultado['beneficio']).update(is_active=False, updated_at=timezone.now())

    @classmethod
    def create_matriculas(cls, cpf, matricula, data, real_time=False):
        try:
            Matricula.objects.create(
                cpf=cpf,
                matricula=matricula
            )
        except IntegrityError:
            pass
        treated_data = MatriculaDetalhadaTreatment(
            data, real_time
        ).treat_and_retrieve()
        treated_data['matricula_id'] = Matricula.objects.get(matricula=matricula)
        MatriculaDetalhada.objects.create(**treated_data)

    @classmethod
    def create_contrato(cls, data, matricula_detalhada, treatment_function, model):
        treated_data = treatment_function(data).treat_and_retrieve()
        for contrato_treated in treated_data:
            contrato_treated['matricula_id'] = matricula_detalhada
            model.objects.create(**contrato_treated)

    @classmethod
    def create_matricula_and_contratos_table(cls, cpf, matricula, data, real_time=False):
        cls.create_matriculas(cpf, matricula, data, real_time=real_time)

        matricula_detalhada = MatriculaDetalhada.objects.get(matricula=matricula)

        cls.create_contrato(data, matricula_detalhada, ContratoEmprestimoTreatment, ContratoEmprestimo)
        cls.create_contrato(data, matricula_detalhada, ContratoCartaoTreatment, ContratoCartao)
