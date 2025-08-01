from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'assigned_caseworker', 'case_notes_count', 'created_at', 'status_indicator')
    list_filter = ('assigned_caseworker', 'created_at', 'updated_at')
    search_fields = ('client_id', 'first_name', 'last_name', 'assigned_caseworker__username', 'assigned_caseworker__first_name', 'assigned_caseworker__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'case_notes_count', 'case_notes_list')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_id', 'first_name', 'last_name')
        }),
        ('Assignment', {
            'fields': ('assigned_caseworker',)
        }),
        ('Case Notes', {
            'fields': ('case_notes_count', 'case_notes_list'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


    def case_notes_count(self, obj):
        """Display count of case notes with link"""
        count = obj.case_notes.count()
        if count > 0:
            url = reverse('admin:case_notes_casenote_changelist') + f'?client__id__exact={obj.id}'
            return format_html(
                '<a href="{}" style="color: #28a745; font-weight: bold;">{} case notes</a>',
                url, count
            )
        return format_html('<span style="color: #6c757d;">No case notes</span>')
    case_notes_count.short_description = 'Case Notes'

    def case_notes_list(self, obj):
        """Display list of recent case notes"""
        case_notes = obj.case_notes.all()[:5]  # Show last 5 notes
        if not case_notes:
            return "No case notes found."
        
        html = '<div style="max-height: 200px; overflow-y: auto;">'
        for note in case_notes:
            html += f'''
                <div style="border: 1px solid #ddd; margin: 5px 0; padding: 10px; border-radius: 4px;">
                    <div style="font-weight: bold; color: #2c5aa0;">
                        {note.created_at.strftime('%Y-%m-%d %H:%M')} - {note.get_interaction_type_display()}
                    </div>
                    <div style="margin-top: 5px; color: #666;">
                        {note.content[:100]}{'...' if len(note.content) > 100 else ''}
                    </div>
                    <div style="margin-top: 5px; font-size: 0.9em; color: #888;">
                        By: {note.created_by.get_full_name() or note.created_by.username}
                    </div>
                </div>
            '''
        html += '</div>'
        return mark_safe(html)
    case_notes_list.short_description = 'Recent Case Notes'

    def status_indicator(self, obj):
        """Show status indicator based on recent activity"""
        recent_notes = obj.case_notes.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7))
        if recent_notes.exists():
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">● Active</span>'
            )
        else:
            return format_html(
                '<span style="color: #ffc107; font-weight: bold;">○ Inactive</span>'
            )
    status_indicator.short_description = 'Status'

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related('assigned_caseworker').prefetch_related('case_notes')

    def get_queryset(self, request):
        """Filter queryset based on user permissions"""
        qs = super().get_queryset(request).select_related('assigned_caseworker').prefetch_related('case_notes')
        if not request.user.is_superuser:
            # For non-superusers, show only their assigned clients
            qs = qs.filter(assigned_caseworker=request.user)
        return qs
