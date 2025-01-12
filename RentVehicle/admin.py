from django.contrib import admin
from .models import RentVehicle
from django.utils.html import format_html

@admin.register(RentVehicle)
class RentVehicleAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = [
        'id', 'Vehicle_license_plate', 'customer_email', 
        'RentVehicle_Date_of_Booking', 'RentVehicle_Date_of_Return', 
        'Total_days', 'Advance_amount', 'RentVehicle_Total_amount', 
        'isAvailable', 'isBillPaid', 'request_status', 'formatted_request_responded_by'
    ]

    # Filters for better data segmentation
    list_filter = [
        'isAvailable', 'isBillPaid', 'request_status', 
        'RentVehicle_Date_of_Booking', 'RentVehicle_Date_of_Return'
    ]

    # Search fields for quick lookups
    search_fields = [
        'Vehicle_license_plate', 'customer_email', 
        'request_responded_by', 'request_status'
    ]

    # Editable fields in the list view
    list_editable = ['isAvailable', 'isBillPaid']

    # Pagination
    list_per_page = 10

    # Fieldsets for better organization
    fieldsets = (
        ('Vehicle Details', {
            'fields': ('Vehicle_license_plate',)
        }),
        ('Customer Details', {
            'fields': ('customer_email',)
        }),
        ('Booking Details', {
            'fields': (
                'RentVehicle_Date_of_Booking', 'RentVehicle_Date_of_Return', 
                'Total_days', 'Advance_amount', 'RentVehicle_Total_amount'
            )
        }),
        ('Request Details', {
            'fields': ('request_status', 'request_responded_by', 'isAvailable', 'isBillPaid')
        }),
    )

    # Actions for bulk updates
    actions = ['mark_as_paid', 'mark_as_unavailable', 'reset_request_status']

    # Adding a custom method for displaying formatted responder
    def formatted_request_responded_by(self, obj):
        if obj.request_responded_by:
            return format_html(
                '<span style="color: green;">{}</span>', obj.request_responded_by
            )
        return format_html('<span style="color: red;">Not Responded</span>')
    formatted_request_responded_by.short_description = "Request Responded By"

    # Admin action to mark all selected as paid
    @admin.action(description="Mark selected vehicles as Bill Paid")
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(isBillPaid=True)
        self.message_user(request, f"{updated} vehicle(s) marked as Bill Paid.")

    # Admin action to mark all selected as unavailable
    @admin.action(description="Mark selected vehicles as Unavailable")
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(isAvailable=False)
        self.message_user(request, f"{updated} vehicle(s) marked as Unavailable.")

    # Admin action to reset the request status to Pending
    @admin.action(description="Reset request status to Pending")
    def reset_request_status(self, request, queryset):
        updated = queryset.update(request_status="Pending")
        self.message_user(request, f"{updated} vehicle(s) request status reset to Pending.")
