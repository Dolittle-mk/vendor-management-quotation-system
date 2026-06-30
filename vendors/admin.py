from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'vendor_name',
        'company_name',
        'email',
        'contact_number',
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'vendor_name',
        'company_name',
        'email',
        'contact_number',
        'business_address'
    ]
    
    list_filter = [
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('vendor_name', 'email', 'contact_number'),
            'classes': ('wide',)
        }),
        ('Company Information', {
            'fields': ('company_name', 'business_address'),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['company_name']
    list_per_page = 25
    
    def get_quotations_count(self, obj):
        return obj.quotation_set.count()
    get_quotations_count.short_description = 'Quotations'