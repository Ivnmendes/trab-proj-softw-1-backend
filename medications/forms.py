from django import forms
from django.core.validators import FileExtensionValidator
from unfold.widgets import UnfoldAdminFileFieldWidget

class ImportMedicationsForm(forms.Form):

    file = forms.FileField(
        label="Arquivo CSV de Medicamentos",
        widget=UnfoldAdminFileFieldWidget(),
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "csv",
                ]
            )
        ],
    )