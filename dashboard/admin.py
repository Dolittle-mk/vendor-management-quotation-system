from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

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
    
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
        'date_joined'
    ]
    
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    
    ordering = ['-date_joined']
    
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} users activated.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} users deactivated.")
    deactivate_users.short_description = "Deactivate selected users"

# Custom Group Admin
class CustomGroupAdmin(GroupAdmin):
    list_display = ['name', 'user_count']
    search_fields = ['name']
    
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Users'

# Unregister default User and Group admin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Register with custom admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# Admin site customization
admin.site.site_header = "Vendor Management System Admin"
admin.site.site_title = "Vendor Management Admin"
admin.site.index_title = "Welcome to Vendor Management System"