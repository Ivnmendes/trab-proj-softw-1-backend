from django.urls import path

from .views import *

urlpatterns = [
    path(
        'admin/import-medications/', 
        import_medications,
        name='import_medications'    
    )
]