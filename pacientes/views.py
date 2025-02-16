from django.shortcuts import render
from django.http import HttpResponse
from .models import Pacientes
# Create your views here.
def pacientes(request):
    #isso aqui ele fala basicamente que quando chamar essa função vai rodar o html
    queixas = Pacientes.queixa_choices
    
    return render(request, 'pacientes.html', {queixas: queixas})