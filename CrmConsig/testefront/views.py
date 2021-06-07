from django.shortcuts import render
from .models import TesteFront
from status.models import Status


def index(request):
    teste = Status.objects.all()
    context = {'teste': teste}
    return render(request, 'teste.html', context)
