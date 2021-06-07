from rest_framework.serializers import ModelSerializer
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo
from envio_sms.models import EnvioSms

from status.models import Status


class MatriculaSerializer(ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'


class MatriculaDetalhadaSerializer(ModelSerializer):
    class Meta:
        model = MatriculaDetalhada
        fields = '__all__'

class EnvioSmsSerializer(ModelSerializer):
    class Meta:
        model = EnvioSms
        fields = '__all__'

class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class ContratoEmprestimoSerializer(ModelSerializer):
    class Meta:
        model = ContratoEmprestimo
        fields = '__all__'
