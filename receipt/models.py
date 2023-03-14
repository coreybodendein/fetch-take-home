import uuid
from django.db import models


class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    points = models.IntegerField()

    def __str__(self):
        return f'{self.id}: {self.points}'
