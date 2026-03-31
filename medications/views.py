from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ImportMedicationsForm
from .services import import_medications_service

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