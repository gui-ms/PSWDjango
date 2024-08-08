from django.contrib import admin
from .models import Documento, Empresas

# Register your models here.

admin.site.register(Empresas)
admin.site.register(Documento)
