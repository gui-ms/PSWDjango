from django.contrib import admin
from .models import Documento, Empresas, Metricas

# Register your models here.

admin.site.register(Empresas)
admin.site.register(Documento)
admin.site.register(Metricas)
