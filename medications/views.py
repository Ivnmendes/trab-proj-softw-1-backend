from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .forms import ImportMedicationsForm
from .models import Medication
from .serializers import MedicationPublicSerializer
from .services import import_medications_service


class MedicationListAPIView(generics.ListAPIView):
    serializer_class = MedicationPublicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Medication.objects.prefetch_related(
            "cids",
            "documents",
            "pharmacies",
        ).order_by("generic_name", "-created_at")


class MedicationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = MedicationPublicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Medication.objects.prefetch_related(
            "cids",
            "documents",
            "pharmacies",
        )


@staff_member_required
def import_medications(request):

    context = admin.site.each_context(request)
    context['title'] = 'Importar Medicamentos'

    if request.method == "POST":

        form = ImportMedicationsForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data["file"]

            message_return, success = import_medications_service(file)

            if success:
                messages.success(request, "Importação Bem Sucedida!")
                return redirect("/admin")
            form.add_error(None, f"Erro ao processar arquivo: {message_return}")
    else:
        form = ImportMedicationsForm()

    context['form'] = form
    return render(request, "import_medications.html", context)