from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.urls import reverse

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    business_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return f"{self.company_name} - {self.vendor_name}"

    def get_absolute_url(self):
        return reverse('vendor_detail', kwargs={'pk': self.pk})

    def get_quotations_count(self):
        return self.quotation_set.count()