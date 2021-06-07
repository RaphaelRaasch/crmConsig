from django.urls import path

from .views import index

app_name = 'data_consig'

urlpatterns = [
    path('', index, name='index'),
]