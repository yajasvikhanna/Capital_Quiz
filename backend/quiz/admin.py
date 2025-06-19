from django.contrib import admin
from .models import Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'capital']
    search_fields = ['name', 'capital']
    list_filter = ['name']
    ordering = ['name']