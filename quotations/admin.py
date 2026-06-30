from django.contrib import admin
from django.utils.html import format_html
from .models import Quotation

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'vendor',
        'reference',
        'amount_display',
        'status_badge',
        'submission_date',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'reference',
        'vendor__company_name',
        'vendor__vendor_name',
        'description'
    ]
    
    list_filter = [
        'status',
        'vendor',
        'submission_date',
        'created_at'
    ]
    
    fieldsets = (
        ('Quotation Details', {
            'fields': ('title', 'description', 'vendor', 'reference', 'amount', 'status'),
            'classes': ('wide',)
        }),
        ('Response Information', {
            'fields': ('response_notes',),
            'classes': ('wide',),
        }),
        ('Timestamps', {
            'fields': ('submission_date', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['submission_date', 'created_at', 'updated_at']
    ordering = ['-submission_date']
    list_per_page = 25
    list_select_related = ['vendor']
    
    def amount_display(self, obj):
        return f"${obj.amount:,.2f}"
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'
    
    def status_badge(self, obj):
        colors = {
            'draft': 'secondary',
            'pending': 'warning',
            'received': 'info',
            'approved': 'success',
            'rejected': 'danger'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'