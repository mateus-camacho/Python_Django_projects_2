from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Pacientes, Tarefas, Consultas, Visualizacoes
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.
def pacientes(request):
    #isso aqui ele fala basicamente que quando chamar essa função vai rodar o html
    if request.method == "GET":
        #pega todos os pacientes do banco
        pacientes = Pacientes.objects.all()
        print(pacientes)
        #como excluir caso tenha feito errado
        # for i in pacientes:
            # i.delete()

        queixas = Pacientes.queixa_choices
        #isso manda para o html as informações
        return render(request, 'pacientes.html', {'queixas': queixas, 'pacientes': pacientes})
    elif request.method == "POST":


        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        queixa = request.POST.get('queixa')
        foto = request.FILES.get('foto')
        
        if len(nome.strip()) == 0 or not foto:
            # apenas um hackzinho pra colocar tarefas no começo em vez de fazer um adimin que esqueci
            # tarefa = Tarefas(
            #     tarefa = "Exercício Físico",
            #     instrucoes = "Faça algum exercício físico para fazer a cabeça não pensar nas coisas e ainda vai ser bom para a saúde    "
            # )
            # tarefa.save()
            messages.add_message(request,constants.ERROR, 'Preencha todos os campos')
            return redirect('pacientes')
        
        paciente = Pacientes(
            nome = nome,
            email=email,
            telefone=telefone,
            queixa=queixa,
            foto=foto
        )
        paciente.save()
        messages.add_message(request,constants.SUCCESS, 'Paciente cadastrado')
        return redirect('pacientes')
    
def paciente_view(request, id):
    paciente = Pacientes.objects.get(id=id)
    if request.method == 'GET':
        tarefas = Tarefas.objects.all()
        consultas = Consultas.objects.filter(paciente=paciente)
        tuple_grafico = ([str(i.data) for i in consultas], [str(i.humor) for i in consultas])
        visualizacoes = Visualizacoes.objects.all()
        return render(request, 'paciente.html', {'paciente' :paciente, 'tarefas' : tarefas, 'consultas': consultas, 'tuple_grafico': tuple_grafico, 'visualizacoes': visualizacoes})
    else:
        humor = request.POST.get('humor')
        registro_geral = request.POST.get('registro_geral')
        video = request.FILES.get('video')
        tarefas = request.POST.getlist('tarefas')
        print(tarefas)
        consultas = Consultas(
            humor=int(humor),
            registro_geral=registro_geral,
            video=video,
            paciente=paciente
        )
        consultas.save()

        for i in tarefas:
            tarefa = Tarefas.objects.get(id=i)
            consultas.tarefas.add(tarefa)

        consultas.save()
        messages.add_message(request, constants.SUCCESS, 'Registro de consulta adicionado com sucesso.')
        return redirect(f'/pacientes/{id}')
    
def atualizar_paciente(request, id):
    paciente = Pacientes.objects.get(id=id)
    pagamento_em_dia = request.POST.get('pagamento_em_dia')
    #TEM que tacar no status se não não funciona
    if pagamento_em_dia == 'ativo': 
        status = True 
    else:
        status = False
    paciente.pagamento_em_dia = status
    paciente.save()
    return redirect(f'/pacientes/{id}')

def excluir_consulta(request, id):
    consulta = Consultas.objects.get(id=id)
    consulta.delete()
    return redirect(f'/pacientes/{consulta.paciente.id}')

def consulta_publica(request, id):
    consulta = Consultas.objects.get(id=id)
    if not consulta.paciente.pagamento_em_dia:
        raise Http404()
    
    view = Visualizacoes(
    consulta=consulta,
    ip=request.META['REMOTE_ADDR']
    )
    view.save()
    return render(request, 'consulta_publica.html', {'consulta': consulta})