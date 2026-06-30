from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Quotation, QuotationHistory
from .forms import QuotationForm, QuotationResponseForm, QuotationCompareForm
from vendors.models import Vendor

@login_required
def quotation_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    quotations = Quotation.objects.all()
    
    if search_query:
        quotations = quotations.filter(
            Q(title__icontains=search_query) |
            Q(reference__icontains=search_query) |
            Q(vendor__company_name__icontains=search_query) |
            Q(vendor__vendor_name__icontains=search_query)
        )
    
    if status_filter:
        quotations = quotations.filter(status=status_filter)
    
    paginator = Paginator(quotations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for stats
    total_quotations = Quotation.objects.count()
    pending_count = Quotation.objects.filter(status='pending').count()
    approved_count = Quotation.objects.filter(status='approved').count()
    rejected_count = Quotation.objects.filter(status='rejected').count()
    received_count = Quotation.objects.filter(status='received').count()
    draft_count = Quotation.objects.filter(status='draft').count()
    
    context = {
        'quotations': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_quotations': total_quotations,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'received_count': received_count,
        'draft_count': draft_count,
    }
    
    return render(request, 'quotations/quotation_list.html', context)

@login_required
def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    history = quotation.history.all()
    context = {
        'quotation': quotation,
        'history': history,
    }
    return render(request, 'quotations/quotation_detail.html', context)

@login_required
def quotation_create(request):
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.save()
            QuotationHistory.objects.create(
                quotation=quotation,
                old_status=quotation.status,
                new_status=quotation.status,
                changed_by=request.user,
                notes="Quotation created"
            )
            messages.success(request, 'Quotation created successfully!')
            return redirect('quotations:quotation_detail', pk=quotation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuotationForm()
        form.fields['status'].initial = 'pending'
    
    context = {'form': form, 'title': 'Create Quotation'}
    return render(request, 'quotations/quotation_form.html', context)

@login_required
def quotation_update(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    old_status = quotation.status
    
    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            quotation = form.save()
            if old_status != quotation.status:
                QuotationHistory.objects.create(
                    quotation=quotation,
                    old_status=old_status,
                    new_status=quotation.status,
                    changed_by=request.user,
                    notes=f"Status updated from {dict(Quotation.Status.choices)[old_status]} to {dict(Quotation.Status.choices)[quotation.status]}"
                )
            messages.success(request, 'Quotation updated successfully!')
            return redirect('quotations:quotation_detail', pk=quotation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuotationForm(instance=quotation)
    
    context = {'form': form, 'title': 'Update Quotation', 'quotation': quotation}
    return render(request, 'quotations/quotation_form.html', context)

@login_required
def quotation_delete(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.method == 'POST':
        quotation.delete()
        messages.success(request, 'Quotation deleted successfully!')
        return redirect('quotations:quotation_list')
    
    context = {'quotation': quotation}
    return render(request, 'quotations/quotation_confirm_delete.html', context)

@login_required
def quotation_response(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    old_status = quotation.status
    
    if request.method == 'POST':
        form = QuotationResponseForm(request.POST, instance=quotation)
        if form.is_valid():
            quotation = form.save()
            if old_status != quotation.status:
                QuotationHistory.objects.create(
                    quotation=quotation,
                    old_status=old_status,
                    new_status=quotation.status,
                    changed_by=request.user,
                    notes=quotation.response_notes or f"Status changed to {dict(Quotation.Status.choices)[quotation.status]}"
                )
            messages.success(request, 'Quotation response submitted successfully!')
            return redirect('quotations:quotation_detail', pk=quotation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuotationResponseForm(instance=quotation)
    
    context = {'form': form, 'quotation': quotation}
    return render(request, 'quotations/quotation_response_form.html', context)

@login_required
def quotation_compare(request):
    if request.method == 'POST':
        form = QuotationCompareForm(request.POST)
        if form.is_valid():
            quotation_ids = form.cleaned_data['quotation_ids']
            quotations = Quotation.objects.filter(id__in=quotation_ids)
            
            if quotations.count() < 2:
                messages.warning(request, 'Please select at least 2 quotations to compare.')
                return redirect('quotations:quotation_compare')
            
            cheapest = quotations.order_by('amount').first()
            
            if quotations.count() > 1:
                amounts = [q.amount for q in quotations]
                max_amount = max(amounts)
                savings = max_amount - cheapest.amount if cheapest else 0
            else:
                savings = 0
            
            context = {
                'quotations': quotations,
                'cheapest': cheapest,
                'savings': savings,
                'form': None,
            }
            return render(request, 'quotations/quotation_compare.html', context)
    else:
        form = QuotationCompareForm()
    
    context = {'form': form}
    return render(request, 'quotations/quotation_compare.html', context)

@login_required
def quotation_history(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    history = quotation.history.all()
    context = {
        'quotation': quotation,
        'history': history,
    }
    return render(request, 'quotations/quotation_history.html', context)