from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authentication.auth import access_basic_required
from data_consig.data_flow import DataFlow

from status.models import Status


@method_decorator([login_required, access_basic_required], name='dispatch')
class CPFView(View):
    template_name = 'cpf.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        cpf = request.POST.get('cpf')
        cleaned_cpf = ''.join(list(filter(lambda x: x.isalnum(), cpf)))
        context = DataFlow(cpf=cleaned_cpf).get_information()
        return render(request, self.template_name, context)


@method_decorator([login_required, access_basic_required], name='dispatch')
class MatriculaDetalhadaView(View):
    template_name = 'matricula_detalhada.html'

    def get(self, request):
        return redirect(reverse('data_consig:cpf_view'))

    def post(self, request):
        matricula = request.POST.get('matricula')
        real_time = bool(request.POST.get('real_time'))
        status = Status.objects.all
        context = DataFlow(matricula=matricula, real_time=real_time, user=request.user.pk).get_information()
        if 'error_msg' in context:
            return redirect(f"/?error_msg={context['error_msg']}")
        return render(request, 'matricula_detalhada.html', context)
