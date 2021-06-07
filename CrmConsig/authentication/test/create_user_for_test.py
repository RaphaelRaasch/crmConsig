from django.contrib.auth import get_user_model

from authentication.models import Usuario, Empresa


class CreateUserForTest:
    def __init__(self):
        self.url_login = '/accounts/login/?next=/auth/'
        self.password = 'password123'

    @staticmethod
    def create_company():
        company = Empresa.objects.create(
            nome='Empresa Teste',
            razao_social='Empresa Teste SA',
            n_user_disponiveis=2,
            email='empresa@empresa.com.br'
        )
        return company.pk

    def create_user(self, user):
        User = get_user_model()
        new_user = User.objects.create_user(username=user, email='user_test@gmail.com', password=self.password)
        return new_user.pk

    def create_custom_user(self, pk: int, role: int, name: str):
        empresa_id = self.create_company()
        Usuario.objects.create(user_id=pk, role=role, name=name, empresa_id=empresa_id)

    def user_basic(self):
        user = 'basic'
        pk = self.create_user(user)
        self.create_custom_user(pk, 444, user)
        return user

    def user_manager(self):
        user = 'manager'
        pk = self.create_user(user)
        self.create_custom_user(pk, 755, user)
        return user

    def user_admin(self):
        user = 'admin'
        pk = self.create_user(user)
        self.create_custom_user(pk, 777, user)
        return user
