// Quotation specific JavaScript

class QuotationManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupStatusFilter();
        this.setupQuotationForm();
        this.setupCompareFeature();
    }

    setupStatusFilter() {
        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter) {
            statusFilter.addEventListener('change', function() {
                this.closest('form').submit();
            });
        }
    }

    setupQuotationForm() {
        const form = document.getElementById('quotationForm');
        if (form) {
            form.addEventListener('submit', function(e) {
                const amount = document.getElementById('id_amount');
                if (amount && parseFloat(amount.value) <= 0) {
                    e.preventDefault();
                    alert('Amount must be greater than 0');
                    amount.focus();
                    return false;
                }
                
                const reference = document.getElementById('id_reference');
                if (reference && reference.value.trim() === '') {
                    e.preventDefault();
                    alert('Reference is required');
                    reference.focus();
                    return false;
                }
            });
        }
    }

    setupCompareFeature() {
        const compareBtn = document.getElementById('compareBtn');
        if (compareBtn) {
            compareBtn.addEventListener('click', function(e) {
                const checked = document.querySelectorAll('input[name="quotation_ids"]:checked');
                if (checked.length < 2) {
                    e.preventDefault();
                    alert('Please select at least 2 quotations to compare');
                }
            });
        }
    }

    calculateTotal(amounts) {
        return amounts.reduce((a, b) => a + b, 0);
    }

    findBestValue(quotations) {
        if (!quotations || quotations.length === 0) return null;
        return quotations.reduce((min, q) => 
            parseFloat(q.amount) < parseFloat(min.amount) ? q : min
        );
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    updateStatusBadge(element, status) {
        const statusMap = {
            'draft': 'secondary',
            'pending': 'warning',
            'received': 'info',
            'approved': 'success',
            'rejected': 'danger'
        };
        
        if (element) {
            element.className = `badge bg-${statusMap[status] || 'secondary'}`;
            element.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
    }

    exportComparisonResults() {
        const table = document.getElementById('comparisonTable');
        if (table) {
            const rows = table.querySelectorAll('tr');
            let csv = [];
            
            rows.forEach(function(row) {
                const cols = row.querySelectorAll('td, th');
                const rowData = [];
                cols.forEach(function(col) {
                    let text = col.innerText.trim();
                    text = text.replace(/\n/g, ' ').replace(/\s+/g, ' ');
                    rowData.push('"' + text + '"');
                });
                csv.push(rowData.join(','));
            });
            
            const csvContent = csv.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.setAttribute('hidden', '');
            a.setAttribute('href', url);
            a.setAttribute('download', 'quotation_comparison.csv');
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }

    autoCompleteReference() {
        const prefix = document.getElementById('referencePrefix');
        const input = document.getElementById('id_reference');
        
        if (prefix && input) {
            const timestamp = new Date().getTime().toString().slice(-6);
            input.value = `${prefix.value}-${timestamp}`;
        }
    }

    validateSubmissionDate() {
        const dateInput = document.getElementById('id_submission_date');
        if (dateInput) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.setAttribute('max', today);
        }
    }
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    const quotationManager = new QuotationManager();
    
    // Auto-complete reference if feature exists
    const refPrefix = document.getElementById('referencePrefix');
    if (refPrefix) {
        quotationManager.autoCompleteReference();
    }
    
    // Validate submission date
    quotationManager.validateSubmissionDate();
});

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuotationManager;
}