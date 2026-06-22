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
    Path = models.TextField('Путь к файлу')
    i = models.FloatField('Сила тока')
    class Meta:
        ordering = ('i',)
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
        ordering = ('name',)
        verbose_name = 'Модель АВР'
        verbose_name_plural = 'Модели АВРов'

    def __str__(self):
        return self.name  