from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Unregister default User and Group admin if they're registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined'
    ]
    
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
        'date_joined'
    ]
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password'),
            'classes': ('wide',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email'),
            'classes': ('wide',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('wide',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['-date_joined']
    
    actions = [
        'activate_users',
        'deactivate_users',
        'make_superuser',
        'remove_superuser'
    ]
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Activated {count} users.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {count} users.")
    deactivate_users.short_description = "Deactivate selected users"
    
    def make_superuser(self, request, queryset):
        count = queryset.update(is_superuser=True, is_staff=True)
        self.message_user(request, f"Made {count} users superusers.")
    make_superuser.short_description = "Make selected users superusers"
    
    def remove_superuser(self, request, queryset):
        count = queryset.update(is_superuser=False)
        self.message_user(request, f"Removed superuser status from {count} users.")
    remove_superuser.short_description = "Remove superuser status"

# Custom Group Admin
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_count']
    search_fields = ['name']
    filter_horizontal = ['permissions']
    
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Users'
    
    actions = ['export_groups']
    
    def export_groups(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="groups_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Group Name', 'User Count', 'Permissions'])
        
        for group in queryset:
            permissions = ', '.join([p.name for p in group.permissions.all()])
            writer.writerow([
                group.name,
                group.user_set.count(),
                permissions
            ])
        
        self.message_user(request, f"Exported {queryset.count()} groups.")
        return response
    export_groups.short_description = "Export selected groups to CSV"

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# Admin site customization
admin.site.site_header = "Vendor Management System"
admin.site.site_title = "Vendor Management Admin"
admin.site.index_title = "Welcome to Vendor Management System"