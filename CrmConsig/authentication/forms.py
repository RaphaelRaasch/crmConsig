from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from authentication.models import Usuario, Empresa, InterestedIn


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('name', 'phone', 'photo', 'role')


class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('name', 'phone', 'photo')


class InterestedUserForm(forms.ModelForm):
    class Meta:
        model = InterestedIn
        fields = ('name', 'phone', 'email')


class UpdateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UpdateUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('name', 'phone', 'photo')


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('name', 'phone', 'photo', 'role')


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('nome', 'razao_social', 'n_user_disponiveis', 'telefone', 'email')
