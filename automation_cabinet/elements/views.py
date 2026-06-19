from django.shortcuts import render
from django.http import JsonResponse
from .models import Automat, Contactor

def baseaup(request):
    return render(request, 'base.html')

def test(request):
    context = []
    contactor = Contactor.objects.all()
    automat = Automat.objects.all()
    context.append(contactor)
    context.append(automat)
    return JsonResponse(
                {"context": context,}
            )
