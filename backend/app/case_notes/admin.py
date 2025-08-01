from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import CaseNote


@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    list_display = ('client_link', 'interaction_type_badge', 'content_preview', 'created_by', 'created_at', 'days_ago')
    list_filter = ('interaction_type', 'created_by', 'created_at', 'client__assigned_caseworker')
    search_fields = ('client__first_name', 'client__last_name', 'client__client_id', 'content', 'created_by__username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'client_link', 'created_by_display')
    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Case Note Information', {
            'fields': ('client', 'content', 'interaction_type')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    def client_link(self, obj):
        """Display client name as a link to client detail"""
        if obj.client:
            url = reverse('admin:clients_client_change', args=[obj.client.id])
            return format_html(
                '<a href="{}" style="color: #2c5aa0; font-weight: bold;">{} ({})</a>',
                url, obj.client.full_name, obj.client.client_id
            )
        return "No client"
    client_link.short_description = 'Client'
    client_link.admin_order_field = 'client__first_name'

    def interaction_type_badge(self, obj):
        """Display interaction type as a colored badge"""
        colors = {
            'phone': '#28a745',
            'in-person': '#007bff',
            'email': '#6f42c1',
            'video': '#fd7e14',
            'other': '#6c757d'
        }
        color = colors.get(obj.interaction_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold;">{}</span>',
            color, obj.get_interaction_type_display()
        )
    interaction_type_badge.short_description = 'Type'
    interaction_type_badge.admin_order_field = 'interaction_type'

    def content_preview(self, obj):
        """Display a preview of the case note content"""
        preview = obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
        return format_html(
            '<div style="max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{}">{}</div>',
            obj.content, preview
        )
    content_preview.short_description = 'Content Preview'

    def created_by_display(self, obj):
        """Display created by with styling"""
        full_name = obj.created_by.get_full_name()
        if full_name:
            return format_html(
                '<strong style="color: #2c5aa0;">{}</strong>',
                full_name
            )
        return format_html(
            '<strong style="color: #2c5aa0;">{}</strong>',
            obj.created_by.username
        )
    created_by_display.short_description = 'Created By'

    def days_ago(self, obj):
        """Show how many days ago the note was created"""
        days = (timezone.now() - obj.created_at).days
        if days == 0:
            return format_html('<span style="color: #28a745;">Today</span>')
        elif days == 1:
            return format_html('<span style="color: #ffc107;">Yesterday</span>')
        elif days < 7:
            return format_html('<span style="color: #fd7e14;">{} days ago</span>', days)
        else:
            return format_html('<span style="color: #6c757d;">{} days ago</span>', days)
    days_ago.short_description = 'Age'
    days_ago.admin_order_field = 'created_at'

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related(
            'client', 'created_by', 'client__assigned_caseworker'
        )

    def get_queryset(self, request):
        """Filter queryset based on user permissions"""
        qs = super().get_queryset(request).select_related(
            'client', 'created_by', 'client__assigned_caseworker'
        )
        if not request.user.is_superuser:
            # For non-superusers, show only case notes for their assigned clients
            qs = qs.filter(client__assigned_caseworker=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        """Automatically set created_by when creating a new case note"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
