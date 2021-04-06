from django.db import models


class Turma(models.Model):
    TURNO = {('M','MANHÃ'),('T','TARDE')}
    turma = models.CharField(max_length=50)
    turno = models.CharField(max_length=50,choices=TURNO, default='M')

    def __str__(self):
        if self.turno == 'M':
            turno_m = 'MANHÃ'
            return self.turma+' - '+ turno_m
        else:
            turno_t = 'TARDE'
            return self.turma+' - '+ turno_t


class Horario(models.Model):
    TIPO = {('U','ÚNICO'),('D','DUPLO')}
    hora_inicio = models.TimeField(verbose_name='Início')
    hora_fim = models.TimeField(verbose_name='Término')
    tipo = models.CharField(max_length=20, verbose_name='Tipo',choices=TIPO, default='U')
    
    
    def __str__(self):
        return str(self.hora_inicio.strftime('%H:%M'))+' - '+str(self.hora_fim.strftime('%H:%M'))
    

class Reserva(models.Model):
    nome= models.CharField(max_length=150)
    email= models.EmailField()
    turma= models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_criacao = models.DateField(auto_now=True, verbose_name='Data da Reserva')
    data= models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, blank=True)
    quantidade = models.IntegerField()
    status = models.BooleanField(verbose_name='Status', auto_created=True, default=True)


    def __str__(self):
        return self.nome