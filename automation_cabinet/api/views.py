"""ViewSet'ы для API."""
import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import AutomatSerializer, RequestSerializer, ResponseSerializer

from elements.models import Automat, Cabinet, ABR


class AutomatViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с Automat."""

    queryset = Automat.objects.all()
    serializer_class = RequestSerializer
    pagination_class = None
    search_fields = ('name',)

def get_i(power):
        return power/220*1000


class VRY():
    otst = 10

    def __init__(self, power, count, checkbox_AVR, outlet, outs):
        self.power = power
        self.count = count
        self.checkbox_AVR = checkbox_AVR
        self.outlet = outlet
        self.outs = outs
        self.elements = []
        self.elements_obj = []
        self.B_min = 0
        self.Y2 = 0
        self.scaf = None
        # self.i = get_i(power)
        self.i = power
        self.generate_input()
        self.generate_output()
        self.getABR()
        
        
        print(self.elements)
    @property    
    def mass(self):
        mass = 0
        for e in self.elements_obj:
            mass= mass+ e.mass
        return mass
    @property    
    def price(self):
        price = 0
        for e in self.elements_obj:
            price= price+ e.price
        return price

    def get_i(power):
        return power/220*1000
        
    def getABR(self):
        if self.checkbox_AVR:
            avr = ABR.objects.filter(i__gte=self.i).order_by('i').first()
            self.elements.append({'path': avr.Path, 'X': self.otst, 'Y': avr.B*1.5, 'Z': 0})
            return True
        return False
    
    def generate_input(self):
        print('adada')
        a = Automat.objects.filter(i__gte=self.i).order_by('i').first()
        print(a)
        if self.count == 2:
            self.B_min = a.B*2*1.3
            self.scaf = Cabinet.objects.filter(B__gte=self.B_min).order_by('mass').first()
            # self.elements.append({'path': self.scaf.Path, 'X': 0, 'Y': 0, 'Z': 0})
            self.elements_obj.append(self.scaf)
            Y = self.scaf.A - a.A
            self.elements.append({'path': a.Path, 'X': (a.B/2 + self.otst), 'Y': Y, 'Z': 0})
            self.elements.append({'path': a.Path, 'X': (self.scaf.B - self.otst - a.B/2), 'Y': Y, 'Z': 0})
            self.elements_obj.append(a)
            self.elements_obj.append(a)
            self.Y2 = Y - a.A*2
            return True
        self.B_min = a.B*1.3
        self.scaf = Cabinet.objects.filter(B__gte=self.B_min).order_by('mass').first()
        
        # self.elements.append({'path': self.scaf.Path, 'X': 0, 'Y': 0, 'Z': 0})
        Y = self.scaf.A - a.A
        self.elements.append({'path': a.Path, 'X': (a.B/2 + self.otst), 'Y': Y, 'Z': 0})
        self.elements_obj.append(self.scaf)
        self.elements_obj.append(a)
        self.elements_obj.append(a)
        return True

    def generate_output(self):
        i = 0
        X=0
        bi =0 
        for e in self.outs:
            a = Automat.objects.filter(i__gte=e['i']).order_by('i').first()
            bi = a.B/2
            if i==0:
                X = a.B/2 + self.otst
            else:
                X = X + bi + a.B/2
            self.elements.append({'path': a.Path, 'X': X, 'Y': self.Y2, 'Z': 0})
            self.elements_obj.append(a)
        # a = Automat.objects.filter(i__gte=self.i).first()
        # if self.count == 2:
        #     self.elements.append(a)
        #     self.elements.append(a)
        #     return True
        # self.elements.append(a)

        return True
    def solve(self):
        if self.count == 2:
                pass
        pass

@api_view(['POST'])
def generate(request):
    serializer = RequestSerializer(data=request.data)
    print(request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    input_data = serializer.data
    
    vry = VRY(
        power=input_data['power'],
        count=input_data['count'],
        checkbox_AVR=input_data['checkbox_AVR'],
        outlet=input_data['outlet'],
        outs=input_data['outs']
    )
    print("Входные данные:", input_data)
    # generated_elements = []

    # element = {
    #         'X': automat.A,
    #         'Y': automat.B,
    #         'Z': automat.C,
    #         'path': automat.Path
    #     }
    # generated_elements.append(element)
    # generated_elements.append(element)

    output_data = {
        'mass': vry.mass,
        'price': vry.price,
        'elements': vry.elements,
        'cabinet': vry.scaf
    }
    print(output_data)
    serializer = ResponseSerializer(output_data)
    return Response(serializer.data, status=200)