"""Административный интерфейс для моделей."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Fiksator, Automat, Cabinet, Contactor

admin.site.register(Fiksator)
admin.site.register(Automat)
admin.site.register(Cabinet)
admin.site.register(Contactor)
# @admin.register(Fiksator)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# @admin.register(Automat)
# class AutomatAdmin(admin.ModelAdmin):
#     list_display = ('name', 'measurement_unit')
#     search_fields = ('name',)