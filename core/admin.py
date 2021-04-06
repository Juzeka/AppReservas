from django.contrib import admin
from core.models import Turma, Horario, Reserva


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display= ['id','turma','turno']     


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display= ['id','hora_inicio','hora_fim', 'tipo']


@admin.register(Reserva)
class Reserva(admin.ModelAdmin):
    list_display=['id','nome','email','turma','data','horario','quantidade','status']
    list_display_links=['id','nome','email','turma','data','horario','quantidade']
    list_editable=['status']
    list_filter=['turma','horario','status']
    ordering= ['horario']
    