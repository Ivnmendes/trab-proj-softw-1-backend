from django.db import models

from core.models import BaseModel
from map.models import Pharmacy

class Medication(BaseModel):

    class Meta:
        verbose_name = "Medicação"
        verbose_name_plural = "Medicações"
        ordering = "generic_name", '-created_at'

    generic_name = models.CharField(
        max_length=255,
        verbose_name="Nome genérico"
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nome"
    )
    description = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Descrição"
    )
    concentration = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Concentração",
    )
    cids = models.ManyToManyField(
        "CID",
        blank=True,
        verbose_name="CID"
    )
    documents = models.ManyToManyField(
        "Document",
        blank=True,
        verbose_name="Documentos"
    )
    pharmacies = models.ManyToManyField(
        Pharmacy,
        blank=True,
        verbose_name="Farmácias"
    )

    def __str__(self):
        if self.name:
            return f"{self.name} - {self.generic_name}"
        return self.generic_name

class CID(BaseModel):

    class Meta:
        verbose_name = "CID"
        verbose_name_plural = "CID's"
        ordering = "name", '-created_at'

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nome"
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Descrição"
    )
    code = models.CharField(
        max_length=5,
        verbose_name="Código do CID"
    )
    documents = models.ManyToManyField(
        "Document",
        verbose_name="Documentos"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

class Document(BaseModel):

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = "name", '-created_at'

    class DocumentType(models.TextChoices):
        IDENTIFICATION = "IDENTIFICATION", "Documentos de identidade"
        REQUEST_FORM = "REQUEST_FORM", "Formulário de solicitação"
        PRESCRIPTION = "PRESCRIPTION", "Receita Médica"
        CLINICAL_REPORT = "CLINICAL_REPORT", "Laudo/Relatório médico"
        LAB_RESULTS = "LAB_RESULTS", "Exames laboratoriais"

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nome"
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Descrição"
    )

    def __str__(self):
        return self.name