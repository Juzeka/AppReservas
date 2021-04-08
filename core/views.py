from django.shortcuts import render,redirect
from .models import Turma,Horario,Reserva
from .forms import ReservaForm
from django.contrib import messages
from django.db.models import Q,Count, Sum
from datetime import date, datetime, timedelta 
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login')
def home(request):
    contexto = {}

    data_atual = date.today()
    hora_atual = datetime.now().strftime('%H:%M:%S')    
    hora= datetime.now()
    hora_chek = timedelta(hours=hora.hour, minutes= hora.minute, seconds=hora.second)   
        
    rs_data = Reserva.objects.all().order_by('data').filter(status=True)
    
    for rs in rs_data:
        rs_fim = timedelta(hours=rs.horario.hora_fim.hour, minutes=rs.horario.hora_fim.minute, seconds=rs.horario.hora_fim.second)
        if rs.data < data_atual:
            rs_data.update(status=False)
        
    
    contexto['data_atual']=data_atual
    contexto['hora_atual']=hora_atual
    contexto['reservas'] = rs_data
    
    qntd_reservada_prox=0
    qntd_reservada=0
    qntd_atual=0

    
    if request.method != 'POST':
        form = ReservaForm(request.POST) 
        contexto['form']= form
        return render(request, 'core/index.html',contexto)
 
    

@login_required(redirect_field_name='login')
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
    print(f'Reserva existe? {rs_status}')
    print(f'Quantidade alocado: {alocado}')
    print(f'Limite de Tablets: {limite}')

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


@login_required(redirect_field_name='login')
def comprovante(request):
    return render (request, 'core/reserva.html')