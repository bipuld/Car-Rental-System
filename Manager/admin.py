from django.contrib import admin
from .models import Manager
from django.utils.html import format_html

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = [
        'id', 'get_full_name', 'Manager_email', 'Manager_mobileno', 
        'Manager_gender', 'Manager_agency', 'Manager_city', 
        'license_preview', 'isOwner'
    ]

    # Filters for easier segmentation
    list_filter = [
        'Manager_gender', 'Manager_agency', 'Manager_city', 
        'Manager_state', 'Manager_country', 'isOwner'
    ]

    # Search functionality
    search_fields = [
        'Manager_firstname', 'Manager_lastname', 'Manager_email', 
        'Manager_mobileno', 'Manager_agency', 'Manager_city', 
        'Manager_state', 'Manager_country'
    ]

    # # Editable fields in the list view
    # list_editable = ['Manager_agency', 'isOwner']

    # Pagination
    list_per_page = 10

    # Read-only fields for better data integrity
    readonly_fields = ['license_preview']

    # Field organization into sections
    fieldsets = (
        ('Personal Information', {
            'fields': ('Manager_firstname', 'Manager_lastname', 'Manager_dob', 'Manager_gender')
        }),
        ('Contact Information', {
            'fields': ('Manager_email', 'Manager_mobileno', 'Manager_address', 'Manager_pincode')
        }),
        ('Agency Details', {
            'fields': ('Manager_agency', 'isOwner')
        }),
        ('Location Details', {
            'fields': ('Manager_city', 'Manager_state', 'Manager_country')
        }),
        ('License Details', {
            'fields': ('Manager_license', 'license_preview')
        }),
    )

    # Adding custom methods for enhanced list view
    def get_full_name(self, obj):
        return f"{obj.Manager_firstname} {obj.Manager_lastname}"
    get_full_name.short_description = "Full Name"

    def license_preview(self, obj):
        if obj.Manager_license:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.Manager_license.url)
        return "No License Uploaded"
    license_preview.short_description = "License Preview"

    # Bulk actions
    actions = ['mark_as_owner', 'unmark_as_owner']

    @admin.action(description="Mark selected managers as Owners")
    def mark_as_owner(self, request, queryset):
        updated = queryset.update(isOwner=True)
        self.message_user(request, f"{updated} manager(s) marked as Owners.")

    @admin.action(description="Unmark selected managers as Owners")
    def unmark_as_owner(self, request, queryset):
        updated = queryset.update(isOwner=False)
        self.message_user(request, f"{updated} manager(s) unmarked as Owners.")
