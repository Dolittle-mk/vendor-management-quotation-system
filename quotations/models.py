from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from vendors.models import Vendor

class Quotation(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending'
        RECEIVED = 'received', 'Received'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    reference = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    submission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    response_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submission_date']

    def __str__(self):
        return f"{self.title} - {self.vendor.company_name}"

    def get_absolute_url(self):
        return reverse('quotations:quotation_detail', kwargs={'pk': self.pk})

    def get_status_badge(self):
        status_colors = {
            'draft': 'secondary',
            'pending': 'warning',
            'received': 'info',
            'approved': 'success',
            'rejected': 'danger',
        }
        return status_colors.get(self.status, 'secondary')
    
    def update_status(self, new_status, user=None):
        """Update status and create history entry"""
        old_status = self.status
        if old_status != new_status:
            self.status = new_status
            self.save()
            # Create history entry
            QuotationHistory.objects.create(
                quotation=self,
                old_status=old_status,
                new_status=new_status,
                changed_by=user,
                notes=f"Status changed from {dict(self.Status.choices)[old_status]} to {dict(self.Status.choices)[new_status]}"
            )
            return True
        return False

class QuotationHistory(models.Model):
    """Track quotation status changes"""
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, choices=Quotation.Status.choices)
    new_status = models.CharField(max_length=20, choices=Quotation.Status.choices)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'Quotation Histories'

    def __str__(self):
        return f"{self.quotation.title} - {self.old_status} to {self.new_status}"