from django.contrib.auth.models import User
from django.db import models

STRING_SMALL = 50
STRING_MEDIUM = 150
STRING_LARGE = 300

ROLE_CHOICES = (
    (777, 'Admin'),
    (755, 'Gerente'),
    (444, 'Usuário comum'),
)


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Empresa(AbstractModel):
    nome = models.CharField(max_length=STRING_MEDIUM)
    razao_social = models.CharField(max_length=STRING_LARGE)
    n_user_disponiveis = models.IntegerField()
    telefone = models.CharField(max_length=STRING_SMALL, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Usuario(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, default=None, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE_CHOICES)
    name = models.CharField('Nome', max_length=STRING_SMALL)
    phone = models.CharField('Telefone', max_length=STRING_SMALL, blank=True)
    photo = models.ImageField("Foto", upload_to='profile', blank=True)
    # TODO  caso necessário para que um usuário tenha um token para acesso via api
    token = models.CharField(max_length=STRING_LARGE, blank=True, null=True, default=False)

    def __str__(self):
        return self.name


class InterestedIn(AbstractModel):
    name = models.CharField('Nome', max_length=STRING_SMALL)
    phone = models.CharField('Telefone', max_length=STRING_SMALL, blank=True)
    email = models.EmailField('E-mail')

    def __str__(self):
        return self.name


class IpBrasil(AbstractModel):
    ip = models.CharField(max_length=STRING_SMALL)