from django.contrib.auth.models import User
from django.db import models


class UploadSms(models.Model):

    PROCESSADO_CHOICES = (
        ('0', 'NAO PROCESSADO'),
        ('1', 'PROCESSADO'),
        ('2', 'ERRO AO PROCESSAR'),
    )

    CAMPANHA_TIPO = (
        ('S', 'S'),
        ('D', 'D'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='sms/')
    pathFile = models.CharField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(max_length=1, choices=PROCESSADO_CHOICES)
    tipo_campanha = models.CharField(max_length=1, choices=CAMPANHA_TIPO)
    total_registros = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nome_campanha = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        self.pathFile = f"{self.file.path}"
        super(UploadSms, self).save(*args, **kwargs)