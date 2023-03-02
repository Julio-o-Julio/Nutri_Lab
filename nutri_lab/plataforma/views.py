from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages import constants
from .models import Paciente, DadosPaciente, Refeicao, Opcao

# Create your views here.

def redirect_pacientes (request):
    if request.method == 'GET':
        return redirect('/pacientes/')

@login_required(login_url='/auth/login/')
def pacientes (request):
    if request.method == 'GET':
        pacientes = Paciente.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/pacientes/')

        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/pacientes/')

        pacientes = Paciente.objects.filter(email=email)

        if pacientes.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/pacientes/')

        try:
            paciente = Paciente(
                nome=nome,
                sexo=sexo,
                idade=idade,
                email=email,
                telefone=telefone,
                nutri=request.user
            )

            paciente.save()

            messages.add_message(request, constants.SUCCESS, 'Paciênte cadastrado com sucesso!')
            return redirect('/pacientes/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema, se for necessário por favor reportar este erro a página de "Ajuda".')
            return redirect('/pacientes/')

@login_required(login_url='/auth/login/')
def dados_paciente_listar(request):
    if request.method == 'GET':
        pacientes = Paciente.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})

@login_required(login_url='/auth/login/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
    if paciente.nutri != request.user:
        messages.add_message(request, constants.ERROR, 'Você não tem acesso aos dados desse paciente!')
        return redirect('/dados_paciente/')
    if request.method == 'GET':
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    elif request.method == 'POST':
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        if len(peso.strip()) == 0 or len(altura.strip()) == 0 or len(gordura.strip()) == 0 or len(musculo.strip()) == 0 or len(hdl.strip()) == 0 or len(ldl.strip()) == 0 or len(colesterol_total.strip()) == 0 or len(triglicerídios.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
            return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})

        try:
            paciente = DadosPaciente(paciente=paciente,
                                    data=datetime.now(),
                                    peso=peso,
                                    altura=altura,
                                    percentual_gordura=gordura,
                                    percentual_musculo=musculo,
                                    colesterol_hdl=hdl,
                                    colesterol_ldl=ldl,
                                    colesterol_total=colesterol_total,
                                    trigliceridios=triglicerídios)

            paciente.save()

            messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')

            return redirect('/dados_paciente/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
            return redirect('/dados_paciente/')

@login_required(login_url='/auth/login/')
@csrf_exempt
def grafico_peso (request, id):
    paciente = Paciente.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by('data')

    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {
        'peso': pesos,
        'labels': labels
    }

    return JsonResponse(data)

def plano_alimentar_listar (request):
    if request.method == 'GET':
        pacientes = Paciente.objects.filter(nutri=request.user)
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})

def plano_alimentar(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
        return redirect('/plano_alimentar_listar/')

    if request.method == 'GET':
        refeicao = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcao = Opcao.objects.all()
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': refeicao, 'opcao': opcao})

def refeicao (request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
        return redirect('/dados_paciente/')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        refeicao = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        refeicao.save()

        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada!')
        return redirect(f'/plano_alimentar/{id_paciente}')

def opcao (request, id_paciente):
    if request.method == 'POST':
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get('descricao')

        opcao = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        opcao.save()

        messages.add_message(request, constants.SUCCESS, 'Opção cadastrada!')
        return redirect(f'/plano_alimentar/{id_paciente}')