from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    public_visibility = models.BooleanField(default=False)
    
    @property
    def age(self):
        from datetime import date
        if self.birth_year:
            today = date.today()
            return today.year - self.birth_year
        return None

class PaymentPending(models.Model):
    name = models.CharField(max_length=255)
    payment_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField()
    agreement_policies = models.TextField()
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Add this line for the signature

    def __str__(self):
        return f"Payment Pending for {self.name}"