from django.contrib import admin
from .models import Vehicle
from django.utils.html import format_html
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = [
        'Vehicle_id', 'Vehicle_name', 'Vehicle_company', 'Vehicle_model',
        'Vehicle_type', 'Vehicle_fuel', 'Vehicle_No_of_Seats', 'Vehicle_color',
        'Vehicle_license_plate', 'isGeared', 'Vehicle_price', 'Vehicle_uploaded_by'
    ]
    def Vehicle_id(self, obj):
        return obj.id

    # Fields editable directly in the list view
    list_editable = ['Vehicle_price', 'Vehicle_color', 'Vehicle_No_of_Seats']

    # Filters to refine the list
    list_filter = [
        'Vehicle_company', 'Vehicle_model', 'Vehicle_type', 'Vehicle_fuel',
        'Vehicle_No_of_Seats', 'Vehicle_color', 'isGeared', 'Vehicle_price'
    ]

    # Fields for searching
    search_fields = [
        'Vehicle_name', 'Vehicle_company', 'Vehicle_model', 'Vehicle_license_plate',
        'Vehicle_uploaded_by'
    ]

    # Pagination
    list_per_page = 10

    # Actions
    actions = ['mark_as_geared', 'mark_as_non_geared']

    # Customizing the form layout
    fieldsets = (
        ('Basic Details', {
            'fields': ('Vehicle_name', 'Vehicle_company', 'Vehicle_model', 'Vehicle_type', 'Vehicle_price')
        }),
        ('Specifications', {
            'fields': ('Vehicle_fuel', 'Vehicle_No_of_Seats', 'Vehicle_color', 'isGeared', 'Vehicle_description')
        }),
        ('Images', {
            'fields': ('Vehicle_image1', 'Vehicle_image2', 'Vehicle_image3')
        }),
        ('License Details', {
            'fields': ('Vehicle_license_plate', 'Vehicle_uploaded_by')
        }),
    )

    # Adding thumbnail previews for images in the list view
    def thumbnail_image1(self, obj):
        if obj.Vehicle_image1:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.Vehicle_image1.url)
        return "No Image"

    thumbnail_image1.short_description = 'Image Preview'
    list_display.insert(9, 'thumbnail_image1')

    # Custom actions
    @admin.action(description="Mark selected vehicles as Geared")
    def mark_as_geared(self, request, queryset):
        updated = queryset.update(isGeared=True)
        self.message_user(request, f'{updated} vehicle(s) marked as Geared.')

    @admin.action(description="Mark selected vehicles as Non-Geared")
    def mark_as_non_geared(self, request, queryset):
        updated = queryset.update(isGeared=False)
        self.message_user(request, f'{updated} vehicle(s) marked as Non-Geared.')
