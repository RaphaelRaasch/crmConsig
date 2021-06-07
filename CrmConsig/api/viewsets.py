from rest_framework.viewsets import ModelViewSet
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo
from envio_sms.models import EnvioSms
from api.serializers import MatriculaSerializer, MatriculaDetalhadaSerializer, EnvioSmsSerializer, StatusSerializer, ContratoEmprestimoSerializer

from status.models import Status


class MatriculaViewSet(ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    filterset_fields = ['cpf']


class MatriculaDetalhadaViewSet(ModelViewSet):
    queryset = MatriculaDetalhada.objects.all()
    serializer_class = MatriculaDetalhadaSerializer
    filterset_fields = ['matricula','cpf']


class ContratoEmprestimoViewSet(ModelViewSet):
    queryset = ContratoEmprestimo.objects.all()
    serializer_class = ContratoEmprestimoSerializer
    filterset_fields = ['matricula']


class EnvioSmsViewSet(ModelViewSet):
    queryset = EnvioSms.objects.all()
    serializer_class = EnvioSmsSerializer
    filterset_fields = ['user_id']


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filterset_fields = ['perfil']
