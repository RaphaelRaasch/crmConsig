from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from authentication.auth import admin_required, access_basic_required, access_manager_required
from authentication.forms import UsuarioForm, UpdateUserForm, UpdateUsuarioForm, AdminUserForm, InterestedUserForm, \
    UsuarioUpdateForm
from authentication.models import Usuario, Empresa, InterestedIn


@method_decorator([login_required, access_basic_required], name='dispatch')
class PerfilUsuarioView(generic.DetailView):
    model = Usuario
    context_object_name = 'user'
    template_name = 'profile.html'


class RegisterUser(generic.CreateView):
    # método Get está implícito
    model = InterestedIn
    template_name = 'registration/login.html'
    form_class = InterestedUserForm
    success_url = '/auth/success_signup/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserModel
        return context


class UpdateUsuario(generic.UpdateView):
    model = Usuario
    context_object_name = 'user'
    template_name = 'profile.html'
    form_class = UsuarioUpdateForm

    def form_valid(self, form):
        form.save()
        return redirect(reverse('auth:user_profile', kwargs={'pk': self.kwargs['pk']}))


@method_decorator([login_required, access_basic_required], name='dispatch')
class AccessBasicView(generic.TemplateView):
    # model = CustomUser
    template_name = 'auth.html'


@method_decorator([login_required, admin_required], name='dispatch')
class AdministrationView(generic.TemplateView):
    template_name = 'auth.html'


@method_decorator([login_required, access_manager_required()], name='dispatch')
class ManagerView(generic.TemplateView):
    template_name = 'auth.html'


@method_decorator([login_required, admin_required], name='dispatch')
class CadastrarUsuarioView(generic.CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'registration/create_user.html'

    def get(self, request, *args, **kwargs):
        user_form = UserCreationForm()
        custom_form = UsuarioForm()
        return render(request, self.template_name, {'custom_form': custom_form, 'user_form': user_form})

    def post(self, request, *args, **kwargs):
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            return self.manage_account(user_form)
        else:
            return render(request, self.template_name, {'custom_form': self.form_class, 'user_form': user_form})

    # def create_custom_user(self, form, user_id):
    #     if UsuarioForm(form).is_valid():
    #         id_user_admin = self.request.user.pk
    #
    #         custom_form = UsuarioForm(self.request.POST, instance=custom)
    #         if custom_form.is_valid():
    #             custom_form.save()
    #             return redirect('/auth/administration')
    #         else:
    #             User.objects.get(pk=user_id).delete()
    #             return HttpResponse('Erro ao criar usuário')

    def manage_account(self, user_form):
        """
        Verifico se a Empresa tem espaço para criar mais usuários
        :param user_form: form para salvar o usuário personalizado
        :return:
        """
        usuario = Usuario.objects.get(user_id=self.request.user.pk)
        empresa = Empresa.objects.get(pk=usuario.empresa_id)
        if empresa.n_user_disponiveis > 0:
            user = user_form.save()
            custom = Usuario.objects.create(user_id=user.pk,
                                            role=self.request.POST['role'],
                                            empresa_id=empresa.pk)
            custom_form = UsuarioForm(self.request.POST, instance=custom)
            if custom_form.is_valid():
                custom_form.save()
                empresa.n_user_disponiveis -= 1
                empresa.save()
                return redirect('/auth/administration')
            else:
                User.objects.get(pk=user.pk).delete()
                return HttpResponse('Erro ao criar usuário')

        else:
            return render(
                self.request, self.template_name,
                {
                    'custom_form': self.form_class, 'user_form': user_form,
                    'msg': 'Limite de usuários execido. '
                           'O seu plano não tem suporte para adicionar mais usuários.',
                    'class': 'alert alert-danger'
                }
            )


@method_decorator([login_required, access_basic_required], name='dispatch')
class AtualizarUserView(generic.UpdateView):
    model = User
    template_name = 'registration/update_user.html'

    def get(self, request, *args, **kwargs):
        pk = self.verify_identify_user()
        if pk:
            user = User.objects.get(pk=pk)
            usuario = Usuario.objects.get(user_id=pk)
            return render(
                request, self.template_name,
                {'user_form': UpdateUserForm(instance=user), 'usuario_form': UpdateUsuarioForm(instance=usuario)}
            )
        else:
            return redirect('403')

    def post(self, request, *args, **kwargs):
        pk = self.verify_identify_user()
        if pk:
            user_form = UpdateUserForm(request.POST, instance=User.objects.get(pk=pk))
            if user_form.is_valid():
                user_form.save()
                return redirect('/auth')
            else:
                return redirect(reverse('auth:user_profile', kwargs={'pk': self.kwargs['pk']}))
        else:
            return redirect('403')

    def verify_identify_user(self):
        pk = self.request.resolver_match.kwargs['pk']
        if self.request.user.pk == int(pk):
            return int(pk)
        else:
            return False


@method_decorator([login_required, admin_required], name='dispatch')
class ListaUsuariosView(generic.ListView):

    def get(self, request, *args, **kwargs):
        users = Usuario.objects.all()
        return render(request, 'listar_usuarios.html', {'users': users})


@method_decorator([login_required, admin_required], name='dispatch')
class AtualizarUsuarioView(generic.UpdateView):
    model = Usuario
    template_name = 'detalhe_usuario.html'
    success_url = '/auth/administration/users'
    form_class = AdminUserForm

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def get_context(self):
        pk = self.request.resolver_match.kwargs['pk']
        usuario = self.model.objects.get(user_id=pk)
        form = AdminUserForm(instance=usuario)
        return {'usuario': usuario, 'form': form}

    def post(self, request, *args, **kwargs):
        context = self.get_context()
        form = AdminUserForm(request.POST, instance=context['usuario'])
        if form.is_valid():
            form.save()
            return redirect('auth:list_user')
        else:
            return render(request, self.template_name, context)


@method_decorator([login_required, admin_required], name='dispatch')
class RemoveUsusario(generic.DeleteView):
    def get(self, request, *args, **kwargs):
        pk = self.request.resolver_match.kwargs['pk']
        user = request.user
        return self.remove_usuario(user, pk)

    def remove_usuario(self, user, pk: str):
        """

        :param user: instância do user que está efetuando ação
        :param pk: id do usuário a ser excluído
        :return:
        """
        if user.pk != int(pk):
            try:
                User.objects.get(pk=pk).delete()
            except IntegrityError:
                return HttpResponse('Erro ao remover esse usuário')
            return redirect('/auth/administration/users')
        else:
            messages.info(self.request, 'Você não pode excluir sua própria conta')
            return redirect(f'/auth/administration/user/{pk}')
