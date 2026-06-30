from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'company_name', 'email', 'contact_number', 'business_address']
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Vendor.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('A vendor with this email already exists.')
        return email