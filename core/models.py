from django.db import models

class BaseModel(models.Model):
    """
    Classe abstrata para fornecer timestamps automáticos
    em todos os modelos do sistema.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em:"    
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em:"    
    )

    class Meta:
        abstract = True