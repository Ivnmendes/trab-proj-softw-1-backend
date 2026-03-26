from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Landmark, Pharmacy

@admin.register(Landmark)
class LandmarkAdmin(ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Pharmacy)
class PharmacyAdmin(ModelAdmin):
    list_display = ('name', 'type', 'address', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at')