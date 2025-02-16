from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pacientes
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.
def pacientes(request):
    #isso aqui ele fala basicamente que quando chamar essa função vai rodar o html
    if request.method == "GET":
        queixas = Pacientes.queixa_choices
        return render(request, 'pacientes.html', {'queixas': queixas})
    elif request.method == "POST":


        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        queixa = request.POST.get('queixa')
        foto = request.FILES.get('foto')
        
        if len(nome.strip()) == 0 or not foto:
            
            return redirect('pacientes')
        
        paciente = Pacientes(
            nome = nome,
            email=email,
            telefone=telefone,
            queixa=queixa,
            foto=foto
        )
        paciente.save()

        return redirect('pacientes')