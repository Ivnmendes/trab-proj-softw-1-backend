from django.db import models

class BaseModel(models.Model):
    """
    Classe abstrata para fornecer timestamps automáticos
    em todos os modelos do sistema.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True