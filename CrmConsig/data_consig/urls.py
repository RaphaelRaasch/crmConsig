from django.urls import path

from .views import CPFView, MatriculaDetalhadaView

app_name = 'data_consig'

urlpatterns = [
    path('', CPFView.as_view(), name='cpf_view'),
    path('informacoes/', MatriculaDetalhadaView.as_view(), name='matricula_detalhada_view'),
]
