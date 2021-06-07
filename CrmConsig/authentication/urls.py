from django.urls import path
from django.views.generic import TemplateView

from authentication import views

app_name = 'auth'

urlpatterns = [
    path('', views.AccessBasicView.as_view(), name='access_basic'),
    path('atualizar/senha/<pk>/', views.AtualizarUserView.as_view(), name='atualizar_senha'),
    path('atualizar/usuario/<pk>/', views.UpdateUsuario.as_view(), name='atualizar_usuario'),
    path('administration/', views.AdministrationView.as_view(), name='administration'),
    path('administration/new_user', views.CadastrarUsuarioView.as_view(), name='new_user'),
    path('administration/users', views.ListaUsuariosView.as_view(), name='list_user'),
    path('administration/update_user/<pk>', views.AtualizarUsuarioView.as_view(), name='user'),
    path('administration/profile/<pk>', views.PerfilUsuarioView.as_view(), name='user_profile'),
    path('administration/delete_user/<pk>', views.RemoveUsusario.as_view(), name='remove_usuario'),
    path('manager/', views.ManagerView.as_view(), name='manager'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path(
        'success_signup/',
        TemplateView.as_view(template_name='success_signup.html'),
        name='success_signup'
    ),
]
