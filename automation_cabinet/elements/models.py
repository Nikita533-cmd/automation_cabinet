from django.db import models

# Create your models here.


class Fiksator(models.Model):
    """Модель крепежа"""

    name = models.CharField('Тип крепления', max_length=150)

    class Meta:
        ordering = ('name',)
        verbose_name = 'крепежа'
        verbose_name_plural = 'крепежи'

    def __str__(self):
        return self.name



class Automat(models.Model):
    """Модель автомата."""
    mass = models.FloatField('Масса, кг')
    price = models.FloatField('Цена, руб')
    name = models.CharField('Название', max_length=150)
    i = models.FloatField('Сила тока')
    Phase = models.IntegerField('Количество фаз')
    A = models.FloatField('Высота')
    B = models.FloatField('Ширина')
    C = models.FloatField('Глубина')
    Path = models.TextField('Путь к файлу')
    fiksator = models.ForeignKey(Fiksator, on_delete = models.CASCADE)
    class Meta:
        ordering = ('i',)
        verbose_name = 'Модель автомата'
        verbose_name_plural = 'Модели автоматов'

    def __str__(self):
        return self.name

class Contactor(models.Model):
    """Модель контактора."""
    mass = models.FloatField('Масса, кг')
    price = models.FloatField('Цена, руб')
    name = models.CharField('Название', max_length=150)
    i = models.FloatField('Сила тока')
    Phase = models.IntegerField('Количество фаз')
    A = models.FloatField('Высота')
    B = models.FloatField('Ширина')
    C = models.FloatField('Глубина')
    Path = models.TextField('Путь к файлу')
    fiksator = models.ForeignKey(Fiksator, on_delete = models.CASCADE)
    class Meta:
        ordering = ('i',)
        verbose_name = 'Модель контактора'
        verbose_name_plural = 'Модели контакторов'

    def __str__(self):
        return self.name  

class Cabinet(models.Model):
    """Модель шкафа."""
    mass = models.FloatField('Масса, кг')
    price = models.FloatField('Цена, руб')
    name = models.CharField('Название', max_length=150)
    A = models.FloatField('Высота')
    B = models.FloatField('Ширина')
    C = models.FloatField('Глубина')
    A_panel = models.FloatField('Высота панели')
    B_panel = models.FloatField('Ширина панели')
    C_panel = models.FloatField('Глубина панели')
    Path = models.TextField('Путь к файлу')
    class Meta:
        ordering = ('mass',)
        verbose_name = 'Модель шкафа'
        verbose_name_plural = 'Модели шкафов'

    def __str__(self):
        return self.name

class ABR(models.Model):
    """Модель АВР."""
    mass = models.FloatField('Масса, кг')
    price = models.FloatField('Цена, руб')
    name = models.CharField('Название', max_length=150)
    A = models.FloatField('Высота')
    B = models.FloatField('Ширина')
    C = models.FloatField('Глубина')
    Path = models.TextField('Путь к файлу')
    fiksator = models.ForeignKey(Fiksator, on_delete = models.CASCADE)
    i = models.FloatField('Сила тока')
    class Meta:
        ordering = ('i',)
        verbose_name = 'Модель АВР'
        verbose_name_plural = 'Модели АВРов'

    def __str__(self):
        return self.name 

from django.contrib.auth.models import AbstractUser
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
    inn = models.IntegerField(
        "ИНН",
        max_length=12,
        null=True,
    )

    kpp = models.IntegerField(
        "КПП",
        max_length=9,
        null=True,
    )
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)