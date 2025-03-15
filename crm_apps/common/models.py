from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    data_criacao = models.DateTimeField(db_index=True, default=timezone.now)
    data_edicao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
