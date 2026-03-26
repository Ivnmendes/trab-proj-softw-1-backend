from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel

class Landmark(BaseModel):

    class Meta:
        verbose_name = "Ponto de Referência"
        verbose_name_plural = "Pontos de Referência"
        ordering = "name", '-created_at'

    name = models.CharField(
        max_length=100, 
        verbose_name="Nome"
    )
    description = models.CharField(
        max_length=500, 
        verbose_name="Descrição"
    )
    latitude = models.DecimalField(
        max_digits=12, 
        decimal_places=9, 
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=12, 
        decimal_places=9, 
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Longitude"
    )
    image = models.ImageField(
        upload_to="landmarks/", 
        null=True, 
        blank=True,
        verbose_name="Imagem"
    )

    def __str__(self):
        return self.name


class Pharmacy(BaseModel):

    class Meta:
        verbose_name = "Farmácia"
        verbose_name_plural = "Farmácias"
        ordering = "name", '-created_at'

    class PharmacyType(models.TextChoices):
        BASIC = "BASIC", "Farmácia Municipal"
        SPECIALIZED = "SPECIALIZED", "Farmácia Estadual"
        POPULAR = "POPULAR", "Farmácia Popular"

    name = models.CharField(
        max_length=100, 
        verbose_name="Nome"
        )
    description = models.CharField(
        max_length=500, 
        verbose_name="Descrição"
        )
    type = models.CharField(
        max_length=20,
        choices=PharmacyType.choices,
        default=PharmacyType.BASIC,
        verbose_name="Tipo"
    )
    address = models.CharField(
        max_length=200,
        verbose_name="Endereço"
    )
    landmark = models.ForeignKey(
        Landmark,
        on_delete=models.CASCADE,
        verbose_name="Localização no Mapa"
    )

    def __str__(self):
        return f"Farmácia: {self.name}"