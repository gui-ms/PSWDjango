from django.http import HttpResponse
from django.shortcuts import redirect, render

from empresarios.models import Documento, Empresas
from .models import PropostaInvestimento
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def sugestao(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    if request.method == 'GET':
        return render(request, 'sugestao.html',{'areas': Empresas.area_choices})
    elif request.method == 'POST':
        tipo = request.POST.get('tipo')
        area = request.POST.getlist('area')
        valor = request.POST.get('valor')

        #Applying more than one filter
        if tipo == 'C':
            empresas = Empresas.objects.filter(tempo_existencia='+5').filter(estagio="E")
        elif tipo == 'D':
            empresas = Empresas.objects.filter(tempo_existencia__in=['-6', '+6', '+1']).exclude(estagio="E")
        
        empresas = empresas.filter(area__in=area)

        empresas_selecionadas = []
        for empresa in empresas:
            percentual = (100*float(valor))/float(empresa.valuation)
            if percentual >= 1:
                empresas_selecionadas.append(empresa)
        
        return render(request, 'sugestao.html',{
            'areas': Empresas.area_choices,
            'empresas': empresas_selecionadas})

def ver_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    documentos = Documento.objects.filter(empresa=empresa)
    return render(request, 'ver_empresa.html', {
        'empresa': empresa,
        'documentos': documentos,
    })

def realizar_proposta(request, id):
    valor = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    empresa = Empresas.objects.get(id=id)

    propostas_aceitas = PropostaInvestimento.objects.filter(empresa=empresa).filter(status='PA')

    total = 0

    for pa in propostas_aceitas:
        total = total + pa.percentual
    
    if total + int(percentual) > empresa.percentual_equity:
        messages.add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo')
        return redirect(f'/investidores/ver_empresa/{id}')
    
    valuation = (100 * int(valor)) / int(percentual)

    if valuation < (int(empresa.valuation) / 2):
        messages.add_message(request, constants.WARNING, f'Seu valuation proposto foi R${valuation} e deve ser no mínimo R${empresa.valuation/2}')
        return redirect(f'/investidores/ver_empresa/{id}')


    pi = PropostaInvestimento(
        valor = valor,
        percentual = percentual,
        empresa = empresa,
        investidor=request.user
    )

    pi.save()

    return redirect(f'/investidores/assinar_contrato/{pi.id}')