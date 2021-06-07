from django.contrib.auth.models import User
from django.shortcuts import render
from django.db import models
from authentication.models import Empresa
from filial.models import Filial
from uploads_sms.models import UploadSms
import requests


class EnvioSms(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    filial_id = models.ForeignKey(Filial, on_delete=models.CASCADE)
    upload_id = models.ForeignKey(UploadSms, on_delete=models.CASCADE, to_field='pathFile')
    # upload_id = models.ForeignKey(UploadSms.pathFile, on_delete=models.CASCADE, to_field='pathFile')
    cpf = models.IntegerField(blank=True, null=True)
    matricula = models.IntegerField(blank=True, null=True)
    celular = models.CharField(max_length=11, blank=True, null=True)
    potencial = models.IntegerField()
    mensagem = models.CharField(max_length=160, blank=True, null=True)
    data_envio = models.DateTimeField(blank=True, null=True)
    id_envio = models.CharField(max_length=155, blank=True)
    status_sms = models.CharField(max_length=3, blank=True)
    resposta = models.CharField(max_length=160, blank=True)
    nr_resposta = models.IntegerField(default=0)
    data_hora_resposta = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        url = 'https://kolmeya.com.br/api/v1/sms/store'

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer y5g8sN3XPkxQ82pNU67x54VC7axKoTeBjU6YzwLd"
        }

        messages = {
            "messages": [
                {
                    "phone": self.celular,
                    "message": f"teste de envio{self.mensagem}",
                }
            ]
        }
        response = requests.post(url=url, headers=headers, json=messages)

        if response.status_code > 200:
            print("Request Failed")

        else:
            self.id_envio = response.json()['id']
            print(response.status_code)
        super(EnvioSms, self).save(*args, **kwargs)




