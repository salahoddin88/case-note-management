from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with case note management features"""
    
    list_display = ('username', 'email', 'employee_id', 'department', 
                   'is_staff', 'is_active', 'assigned_clients_count', 'recent_activity')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'department', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'employee_id')
    ordering = ('username',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('employee_id', 'phone_number', 'department')
        }),
        ('Case Note Management', {
            'fields': ('assigned_clients_count', 'recent_activity'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = BaseUserAdmin.readonly_fields + ('assigned_clients_count', 'recent_activity', 'created_at', 'updated_at')

    
    def assigned_clients_count(self, obj):
        """Show count of assigned clients"""
        if hasattr(obj, 'assigned_clients'):
            count = obj.assigned_clients.count()
            if count > 0:
                url = reverse('admin:clients_client_changelist') + f'?assigned_caseworker__id__exact={obj.id}'
                return format_html(
                    '<a href="{}" style="color: #28a745; font-weight: bold;">{} assigned clients</a>',
                    url, count
                )
        return format_html('<span style="color: #6c757d;">No assigned clients</span>')
    assigned_clients_count.short_description = 'Assigned Clients'
    
    def recent_activity(self, obj):
        """Show recent case note activity"""
        if hasattr(obj, 'created_case_notes'):
            recent_notes = obj.created_case_notes.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            if recent_notes > 0:
                return format_html(
                    '<span style="color: #28a745; font-weight: bold;">{} case notes in last 7 days</span>',
                    recent_notes
                )
        return format_html('<span style="color: #6c757d;">No recent activity</span>')
    recent_activity.short_description = 'Recent Activity'
    
    def get_queryset(self, request):
        """Optimize queryset with related data"""
        qs = super().get_queryset(request)
        if hasattr(qs.model, 'assigned_clients'):
            qs = qs.prefetch_related('assigned_clients')
        if hasattr(qs.model, 'created_case_notes'):
            qs = qs.prefetch_related('created_case_notes')
        return qs