// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const dismissBtn = alert.querySelector('.btn-close');
            if (dismissBtn) {
                dismissBtn.click();
            }
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Confirm delete
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Enable tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(function(tooltip) {
        new bootstrap.Tooltip(tooltip);
    });

    // ===== FIX: Search with Enter key only (NO AUTO-SUBMIT) =====
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(function(input) {
        // Remove ALL existing event listeners by cloning
        const newInput = input.cloneNode(true);
        input.parentNode.replaceChild(newInput, input);
        
        // Only submit on Enter key press
        newInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
        
        // Prevent any other key from submitting
        newInput.addEventListener('keyup', function(e) {
            // Do nothing - this prevents auto-submit
            e.stopPropagation();
        });
        
        // Prevent input event from submitting
        newInput.addEventListener('input', function(e) {
            // Do nothing - this prevents auto-submit on typing
            e.stopPropagation();
        });
    });

    // ===== Fix: Search button should submit the form =====
    const searchButtons = document.querySelectorAll('button[type="submit"]');
    searchButtons.forEach(function(button) {
        const form = button.closest('form');
        if (form && form.querySelector('input[name="search"]')) {
            // Remove any existing click handlers
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
            
            newButton.addEventListener('click', function(e) {
                e.preventDefault();
                const searchForm = this.closest('form');
                if (searchForm) {
                    searchForm.submit();
                }
            });
        }
    });

    // ===== Fix: Status filter dropdown (for quotations) =====
   const statusFilter = document.getElementById('quotationStatusFilter');
if (statusFilter) {
    const form = statusFilter.closest('form');
    if (form) {
        const newFilter = statusFilter.cloneNode(true);
        statusFilter.parentNode.replaceChild(newFilter, statusFilter);

        newFilter.addEventListener('change', function() {
            const parentForm = this.closest('form');
            if (parentForm) {
                parentForm.submit();
            }
        });
    }
}

    // Admin badge tooltips
    const adminBadges = document.querySelectorAll('.admin-badge');
    adminBadges.forEach(function(badge) {
        badge.setAttribute('data-bs-toggle', 'tooltip');
        badge.setAttribute('data-bs-placement', 'bottom');
        badge.setAttribute('title', 'You have administrator privileges');
        new bootstrap.Tooltip(badge);
    });

    // Back to top button
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (backToTopBtn) {
        window.onscroll = function() {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                backToTopBtn.style.display = "block";
            } else {
                backToTopBtn.style.display = "none";
            }
        };
    }
});

// Print function
function printPage() {
    window.print();
}

// Export to CSV
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
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
    a.setAttribute('download', filename + '.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Toast notifications
function showToast(title, message, type) {
    type = type || 'success';
    var colors = {
        success: 'bg-success text-white',
        danger: 'bg-danger text-white',
        warning: 'bg-warning text-dark',
        info: 'bg-info text-white'
    };
    
    var icons = {
        success: 'fa-check-circle',
        danger: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    var toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    var toast = document.createElement('div');
    toast.className = 'toast align-items-center ' + (colors[type] || colors.info) + ' border-0 show';
    toast.role = 'alert';
    toast.innerHTML = 
        '<div class="d-flex">' +
            '<div class="toast-body">' +
                '<i class="fas ' + (icons[type] || icons.info) + ' me-2"></i>' +
                '<strong>' + title + '</strong> - ' + message +
            '</div>' +
            '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>' +
        '</div>';
    toastContainer.appendChild(toast);
    
    setTimeout(function() {
        toast.remove();
    }, 4000);
}

// Console welcome message
console.log('%c Vendor Quotation System ', 'background: #0d6efd; color: white; font-size: 16px; padding: 10px; border-radius: 5px;');
console.log('%c Welcome to the Vendor Management & Quotation System! ', 'color: #0d6efd; font-size: 14px;');