from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML
import tempfile
from django.utils.encoding import escape_uri_path
from .models import User, CalculateResult, MPNYResult, IPAResult
from .serializers import UserSerializer
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get("username", None)
        password = data.get("password", None)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


def login_as(request, user):
    if request.user.is_superuser:
        user = User.objects.get(pk=user)
        login(request, user)
    return redirect("/admin/")


class SaveCalculationResultAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        print('user:', request.user)
        print('user:', request.user.is_authenticated)
        print('data:717171717171771717', data)
        # Создаем запись с результатами расчета
        calculate_result = CalculateResult.objects.create(
            user=request.user if request.user.is_authenticated else None,
            data=data,
            name_object=data['name_object'],
            address_object=data['address_object'],
        )
        print
        print('user:', request.user)
        print('user:', request.user.is_authenticated)

        return Response(
            {
                "id": str(calculate_result.id),
                "message": "Результаты успешно сохранены",
                "redirect_url": f"/users/calculation-result/{calculate_result.id}/pdf/"
            },
            status=status.HTTP_201_CREATED
        )


def calculation_result_view(request, result_id):
    """Отображение сохраненных результатов расчета"""
    result = get_object_or_404(CalculateResult, id=result_id)
    return render(request, 'users/calculation_result_pdf.html', {'result': result})


def calculation_result_pdf(request, result_id):
    """Экспорт результатов расчета в PDF"""
    result = get_object_or_404(CalculateResult, id=result_id)

    # Рендерим HTML шаблон
    html_string = render_to_string('users/calculation_result_pdf.html', {'result': result})

    # Создаем PDF из HTML
    try:
        # Создаем HTML объект и генерируем PDF
        html_obj = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_bytes = html_obj.write_pdf()
    except Exception as e:
        # В случае ошибки возвращаем сообщение с деталями
        import traceback
        error_detail = traceback.format_exc()
        return HttpResponse(f"Ошибка при генерации PDF: {str(e)}\n\n{error_detail}", status=500, content_type='text/plain')

    # Формируем имя файла
    filename = f"calculation_result_{result.id}.pdf"

    # Возвращаем PDF файл
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

# def get_pdf(request, result_id):
#     """Экспорт результатов расчета в PDF"""
#     result = get_object_or_404(MPNYResult, id=result_id)

#     # Рендерим HTML шаблон
#     # html_string = render_to_string('users/calculation_result_pdf.html', {'result': result})
#     html_string = render_to_string("users/mpnu_pdf.html", result.data)
#     pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
#     response = HttpResponse(pdf, content_type='application/pdf')
#     filename = f"{result.name}.pdf"
#     response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(filename)}"'
#     return response

# def get_pdf_ipa(request, result_id):
#     """Экспорт результатов расчета в PDF"""
#     result = get_object_or_404(IPAResult, id=result_id)
#     html_string = render_to_string("users/ipa_pdf.html", result.data)
#     pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
#     response = HttpResponse(pdf, content_type="application/pdf")
#     return response
# from django.core.mail import EmailMultiAlternatives
# def get_tkp_mpny(request, result_id):
#     """Экспорт результатов расчета в PDF"""
#     result = get_object_or_404(MPNYResult, id=result_id)

#     # Рендерим HTML шаблон
#     # html_string = render_to_string('users/calculation_result_pdf.html', {'result': result})
#     html_string = render_to_string("users/mpnu_pdf.html", result.data)
#     pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
#     response = HttpResponse(pdf, content_type='application/pdf')
#     filename = f"{result.name}.pdf"
#     response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(filename)}"'
#     email = EmailMessage(
#         subject=f"PDF {result.name}",
#         body=f"Добрый день! Направляю Вам технические параметры для подготовки технико-коммерческого предложения (ТКП) на изготовление изделия. Файл с результатами предварительного расчета со всеми необходимыми характеристиками находится во вложении к этому письму (в формате PDF). С уважением, {request.user}",
#         from_email=os.getenv('from_email', 'info@sa-biysk.ru'),
#         to=os.getenv("to_email").split(', '),
#         reply_to=[request.user.email]
#     )
#     print ('email.from_email', email.from_email)
#     # # html = render_to_string('test.html')
#     # email = EmailMultiAlternatives(
#     #             subject=f"PDF {result.name}",
#     #             body=html,
#     #             from_email=os.getenv('from_email', 'info@sa-biysk.ru'),
#     #             to=os.getenv("to_email").split(', '),
#     #             reply_to=[request.user.email]
#     #         )
#     # email.attach_alternative(html, "text/html")
#     email.attach(f"{result.name}.pdf", pdf, "application/pdf")
#     email.send(fail_silently=False)
#     return JsonResponse({'message': "Сообщение отправлено"}, status=201)
