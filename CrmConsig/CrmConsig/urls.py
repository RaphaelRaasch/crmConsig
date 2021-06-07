from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from api import viewsets
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'matricula', viewsets.MatriculaViewSet)
router.register(r'matriculaDetalhada', viewsets.MatriculaDetalhadaViewSet)
router.register(r'contratoemprestimo', viewsets.ContratoEmprestimoViewSet)
router.register(r'EnvioSms', viewsets.EnvioSmsViewSet)
router.register(r'status', viewsets.StatusViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('data_consig.urls'), name='data_consig'),
    path('auth/', include('authentication.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('403', TemplateView.as_view(template_name='403.html'), name='403'),
    path('testes/', include('testefront.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('500', TemplateView.as_view(template_name='500.html'), name='500'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



