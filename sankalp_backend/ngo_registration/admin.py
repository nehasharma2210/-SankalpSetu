from django.contrib import admin
from .models import NGO, NGODocument

@admin.register(NGO)
class NGOAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'city', 'state', 'status', 
        'registration_number', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'state', 'country', 'created_at'
    ]
    search_fields = [
        'name', 'registration_number', 'email', 'city', 'description'
    ]
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'website', 'status')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Address Information', {
            'fields': (
                'address_line1', 'address_line2', 'city', 
                'state', 'postal_code', 'country'
            )
        }),
        ('Legal Information', {
            'fields': (
                'registration_number', 'registration_date', 
                'tax_exempt_number'
            )
        }),
        ('Additional Information', {
            'fields': (
                'founding_year', 'employee_count', 'annual_budget'
            )
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by')

@admin.register(NGODocument)
class NGODocumentAdmin(admin.ModelAdmin):
    list_display = [
        'ngo', 'document_type', 'document_name', 'uploaded_at'
    ]
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['ngo__name', 'document_name']
    readonly_fields = ['uploaded_at']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('ngo')
