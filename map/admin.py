from django.contrib import admin
from .models import Landmark, Pharmacy

@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'address', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at')