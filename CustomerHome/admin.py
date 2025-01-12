from django.contrib import admin
from .models import Customer
from django.utils.html import format_html

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = [
        'id', 'get_full_name', 'customer_email', 'customer_mobileno', 
        'customer_gender', 'customer_city', 'customer_state', 'license_preview'
    ]

    # Filters for better data segmentation
    list_filter = ['customer_gender', 'customer_city', 'customer_state', 'customer_country']

    # Search functionality
    search_fields = [
        'customer_firstname', 'customer_lastname', 'customer_email', 
        'customer_mobileno', 'customer_city', 'customer_state', 'customer_country'
    ]

    # # Editable fields in the list view
    # list_editable = ['customer_mobileno', 'customer_city', 'customer_state']

    # Pagination
    list_per_page = 10

    # Read-only fields in the form
    readonly_fields = ['license_preview']

    # Form layout customization
    fieldsets = (
        ('Personal Information', {
            'fields': ('customer_firstname', 'customer_lastname', 'customer_dob', 'customer_gender')
        }),
        ('Contact Information', {
            'fields': ('customer_email', 'customer_mobileno', 'customer_address', 'customer_pincode')
        }),
        ('Location Details', {
            'fields': ('customer_city', 'customer_state', 'customer_country')
        }),
        ('License Details', {
            'fields': ('customer_license', 'license_preview')
        }),
    )

    # Custom methods for displaying additional information
    def get_full_name(self, obj):
        return f"{obj.customer_firstname} {obj.customer_lastname}"
    get_full_name.short_description = "Full Name"

    def license_preview(self, obj):
        if obj.customer_license:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.customer_license.url)
        return "No License Uploaded"
    license_preview.short_description = "License Preview"

    # Bulk actions
    actions = ['mark_as_female', 'mark_as_male', 'mark_as_other']

    @admin.action(description="Mark selected customers as Female")
    def mark_as_female(self, request, queryset):
        updated = queryset.update(customer_gender='Female')
        self.message_user(request, f"{updated} customer(s) marked as Female.")

    @admin.action(description="Mark selected customers as Male")
    def mark_as_male(self, request, queryset):
        updated = queryset.update(customer_gender='Male')
        self.message_user(request, f"{updated} customer(s) marked as Male.")

    @admin.action(description="Mark selected customers as Other")
    def mark_as_other(self, request, queryset):
        updated = queryset.update(customer_gender='Other')
        self.message_user(request, f"{updated} customer(s) marked as Other.")
