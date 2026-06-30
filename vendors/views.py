from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vendor
from .forms import VendorForm

@login_required
def vendor_list(request):
    search_query = request.GET.get('search', '')
    vendors = Vendor.objects.all()
    
    if search_query:
        vendors = vendors.filter(
            Q(vendor_name__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    paginator = Paginator(vendors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'vendors': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'vendors/vendor_list.html', context)

@login_required
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    quotations = vendor.quotation_set.all()
    context = {
        'vendor': vendor,
        'quotations': quotations,
    }
    return render(request, 'vendors/vendor_detail.html', context)

@login_required
def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor created successfully!')
            return redirect('vendors:vendor_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VendorForm()
    
    context = {'form': form, 'title': 'Add Vendor'}
    return render(request, 'vendors/vendor_form.html', context)

@login_required
def vendor_update(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor updated successfully!')
            return redirect('vendors:vendor_detail', pk=vendor.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VendorForm(instance=vendor)
    
    context = {'form': form, 'title': 'Update Vendor', 'vendor': vendor}
    return render(request, 'vendors/vendor_form.html', context)

@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        messages.success(request, 'Vendor deleted successfully!')
        return redirect('vendors:vendor_list')
    
    context = {'vendor': vendor}
    return render(request, 'vendors/vendor_confirm_delete.html', context)