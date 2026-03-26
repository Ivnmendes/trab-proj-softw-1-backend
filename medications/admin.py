from django.contrib import admin
from .models import Medication, CID, Document

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('generic_name', 'name', 'concentration', 'created_at')
    list_filter = ('pharmacies', 'created_at')
    search_fields = ('name', 'generic_name', 'components')
    filter_horizontal = ('cids', 'documents', 'pharmacies')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CID)
class CIDAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'created_at')
    search_fields = ('code', 'name')
    filter_horizontal = ('documents',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at', 'updated_at')