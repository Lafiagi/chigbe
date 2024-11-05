from django.db import models
from generics.base_model import BaseModel


class Drug(BaseModel):
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    batch_number = models.CharField(max_length=50)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    manufacturer = models.CharField(max_length=255)
    unique_code = models.CharField(max_length=50, unique=True, blank=True)
    owner = models.ForeignKey("authy.User", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.dosage} manufactured on {self.manufacture_date}"
