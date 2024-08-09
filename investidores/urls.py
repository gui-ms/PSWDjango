from django.urls import path, include
from . import views

urlpatterns = [
    path('sugestao/',views.sugestao, name='sugestao'),
]