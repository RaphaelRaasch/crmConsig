from django.db import models


class TesteFront(models.Model):
    teste = models.CharField(max_length=12)
    descricao = models.CharField(max_length=12)

    def __str__(self):
        return self.teste