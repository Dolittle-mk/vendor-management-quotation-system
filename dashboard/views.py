from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from vendors.models import Vendor
from quotations.models import Quotation, QuotationHistory

@login_required
def dashboard(request):
    # Total Vendors
    total_vendors = Vendor.objects.count()
    
    # Quotation statistics
    total_quotations = Quotation.objects.count()
    active_quotations = Quotation.objects.filter(status__in=['pending', 'received']).count()
    pending_quotations = Quotation.objects.filter(status='pending').count()
    approved_quotations = Quotation.objects.filter(status='approved').count()
    rejected_quotations = Quotation.objects.filter(status='rejected').count()
    draft_quotations = Quotation.objects.filter(status='draft').count()
    received_quotations = Quotation.objects.filter(status='received').count()
    
    # Recent quotations (last 5)
    recent_quotations = Quotation.objects.all().order_by('-created_at')[:5]
    
    # Recent vendors (last 5)
    recent_vendors = Vendor.objects.all().order_by('-created_at')[:5]
    
    # Recent Activities (Quotation History)
    recent_activities = QuotationHistory.objects.select_related('quotation', 'changed_by').all().order_by('-changed_at')[:10]
    
    # Quotations by status for chart
    status_data = Quotation.objects.values('status').annotate(count=Count('status'))
    
    # Quotations by vendor (top 5)
    vendor_data = Quotation.objects.values('vendor__company_name').annotate(
        count=Count('vendor')
    ).order_by('-count')[:5]
    
    context = {
        'total_vendors': total_vendors,
        'total_quotations': total_quotations,
        'active_quotations': active_quotations,
        'pending_quotations': pending_quotations,
        'approved_quotations': approved_quotations,
        'rejected_quotations': rejected_quotations,
        'draft_quotations': draft_quotations,
        'received_quotations': received_quotations,
        'recent_quotations': recent_quotations,
        'recent_vendors': recent_vendors,
        'recent_activities': recent_activities,
        'status_data': list(status_data),
        'vendor_data': list(vendor_data),
    }
    
    return render(request, 'dashboard/dashboard.html', context)