from django.urls import path

from .views import *

urlpatterns = [
    path(
        "api/",
        MedicationListAPIView.as_view(),
        name="medication-list-api",
    ),
    path(
        "api/<int:pk>/",
        MedicationDetailAPIView.as_view(),
        name="medication-detail-api",
    ),
    path(
        'admin/import-medications/', 
        import_medications,
        name='import_medications'    
    )
]