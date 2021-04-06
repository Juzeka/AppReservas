from django.shortcuts import render,redirect
from core.forms import ReservaForm
from .models import Turma,Horario,Reserva
from .forms import ReservaForm
from django.contrib import messages
from django.db.models import Q,Count, Sum
from datetime import date, datetime
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def home(request):
    contexto = {}

    data_atual = date.today()
    hora_atual = datetime.now().strftime('%H:%M:%S')
    futuro = date.fromordinal(data_atual.toordinal()+3)
    
        
    rs_data = Reserva.objects.all().order_by('data').filter(status=True)
    queryset = Reserva.objects.raw('SELECT core_reserva.id, core_reserva.nome, core_reserva.email, core_reserva.turma_id, core_reserva.data, core_reserva.horario_id, core_reserva.quantidade, SUM(core_reserva.quantidade) AS quantidade__sum FROM core_reserva WHERE (core_reserva.data = 2021-04-01 OR core_reserva.data >= 2021-04-04) GROUP BY core_reserva.data ORDER BY NULL')

    contexto['data_atual']=data_atual
    contexto['hora_atual']=hora_atual
    contexto['reservas'] = rs_data
    
    qntd_reservada_prox=0
    qntd_reservada_futuro=0
    qntd_reservada=0
    qntd_atual=0

    somatorio=[]
    for qs in queryset:
        disponibilidade = {
            'data': qs.data,
            'quantidade': 45-qs.quantidade__sum,
            'alocados': qs.quantidade__sum 
        }
        
        somatorio.append(disponibilidade)
    if request.method != 'POST':
        form = ReservaForm(request.POST) 
        contexto['form']= form
        contexto['somatorio'] = somatorio
        return render(request, 'core/index.html',contexto)
    
    return render (request, 'core/index.html',{'somatorio':somatorio})
 
    


def reservar(request):
    form = ReservaForm(request.POST)
    data_atual = date.today()
    contexto={}    

    data= request.POST.get('data')
    horario =request.POST.get('horario')
    turma = request.POST.get('turma')
    qntd = int(request.POST.get('quantidade'))
    rs_date_hous_turma = Reserva.objects.filter(data=data, horario=horario, turma= turma, status=True).exists()
    rs_date = Reserva.objects.filter(data=data, horario=horario, status=True)
    rs_turma = Reserva.objects.filter( turma=turma, status=True).exists()
    rs_status = Reserva.objects.filter(data=data, horario=horario, turma=turma, status=True).exists()
    alocado =0
    for s in rs_date:
        alocado+=s.quantidade
    
    limite= alocado+qntd

    if  str(data_atual) > data:
        messages.add_message(request,messages.ERROR, 'Impossível registrar datas passadas')
        return redirect('home')

    if rs_date_hous_turma:
        messages.add_message(request,messages.ERROR, 'Reserva já existente.')
        return redirect('home')      

    if rs_date_hous_turma == False and limite <= 45 and form.is_valid():
        form.save()
        quereset = Reserva.objects.get(data=data, horario=horario, turma=turma, status=True)
        comprovante = {
            'nome':quereset.nome,
            'email':quereset.email,
            'turma':quereset.turma,
            'data':quereset.data,
            'horario':quereset.horario,
            'quantidade':quereset.quantidade,
        }
        messages.add_message(request,messages.SUCCESS, 'Reserva feita com sucesso')
        return render(request, 'core/reserva.html',comprovante)
    elif limite > 45:
        messages.add_message(request,messages.ERROR, 'Quantidade de tablets indisponível.')
        return redirect('home')      
        
    
    messages.add_message(request,messages.ERROR, 'Erro ao fazer reserva.')
    return redirect('home')    



def comprovante(request):
    
    return render (request, 'core/reserva.html')