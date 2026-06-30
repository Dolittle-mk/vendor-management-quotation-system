from django import forms
from .models import Quotation
from vendors.models import Vendor

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['title', 'description', 'vendor', 'reference', 'amount', 'status', 'response_notes']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'response_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor'].queryset = Vendor.objects.all().order_by('company_name')
        self.fields['status'].required = False
        self.fields['response_notes'].required = False

    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        if Quotation.objects.filter(reference=reference).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('A quotation with this reference already exists.')
        return reference

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        return amount

class QuotationResponseForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['response_notes', 'status']
        widgets = {
            'response_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter your response notes here...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response_notes'].required = True
        self.fields['status'].required = True

class QuotationCompareForm(forms.Form):
    quotation_ids = forms.ModelMultipleChoiceField(
        queryset=Quotation.objects.filter(status__in=['received', 'approved']),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label='Select Quotations to Compare'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quotation_ids'].queryset = Quotation.objects.filter(
            status__in=['received', 'approved']
        ).order_by('-submission_date')