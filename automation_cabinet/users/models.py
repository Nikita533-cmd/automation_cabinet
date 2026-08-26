import uuid
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    first_name = models.CharField("Имя", max_length=100, null=True)
    last_name = models.CharField(
        "Фамилия",
        max_length=100,
        null=True,
    )
    parent_name = models.CharField(
        "Отчество",
        max_length=100,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=250,
        verbose_name='почта'
    )
    phone = PhoneNumberField(
        verbose_name='телефон',
        null=True,
    )

    organization = models.CharField(
        "Организация",
        max_length=100,
        null=True,
    )
    inn = models.BigIntegerField(
        "ИНН",        
        null=True,
    )

    kpp = models.BigIntegerField(
        "КПП",        
        null=True,
    )
    city = models.CharField(
        "Город",
        max_length=100,
        null=True,
    )
    job_title = models.CharField(
        "Должность",
        max_length=100,
        null=True,
    )
    agreement = models.BooleanField(
        "Подтверждение об ознакомлении с политикой защиты и обработки персональных данных",
        default=False,        
    )
    agreement_2 = models.BooleanField(
        "Согласие на обработку персональных данных",
        default=False,        
    )
    # date_joined = models.DateField(
    #     "Дата регистрации",
    #     max_length=100,
    #     null=True,
    # )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    @property
    def fio(self):
        return " ".join((self.last_name, self.first_name, self.parent_name))

    @property
    def ini(self):
        if not self.first_name or not self.parent_name:
            return self.last_name
        return f"{self.last_name} {self.first_name[0]}.{self.parent_name[0]}."


class UserGroup(Group):
    # только для админки

    class Meta:
        proxy = True
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class CalculateResult(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    data = models.JSONField(verbose_name="Данные расчета", default=dict)

    name_object = models.CharField(
        "Наименование объекта",
        max_length=1000,
        null=True,
    )
    address_object = models.CharField(
        "Наименование адрес",
        max_length=1000,
        null=True,
    )

    class Meta:
        verbose_name = "Результат расчета"
        verbose_name_plural = "Результаты расчетов"

    def __str__(self):
        user_info = self.user.ini if self.user else "Анонимный"
        return f"Результат расчета #{self.id} пользователя {user_info} от {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_absolute_url(self):
        return reverse("users:calculation_result", args=[str(self.id)])
    

