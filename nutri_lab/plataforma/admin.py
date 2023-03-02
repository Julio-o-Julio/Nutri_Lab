from django.contrib import admin
from .models import Paciente, DadosPaciente, Opcao, Refeicao

# Register your models here.

admin.site.register(Paciente)
admin.site.register(DadosPaciente)
admin.site.register(Opcao)
admin.site.register(Refeicao)