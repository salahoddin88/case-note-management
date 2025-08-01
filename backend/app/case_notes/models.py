import uuid
from django.db import models
from django.conf import settings
from clients.models import Client


class CaseNote(models.Model):
    """Model for storing case notes for client interactions."""
    
    INTERACTION_TYPES = [
        ('phone', 'Phone Call'),
        ('in-person', 'In-Person Meeting'),
        ('email', 'Email'),
        ('video', 'Video Call'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='case_notes'
    )
    content = models.TextField(help_text="Detailed notes about the client interaction")
    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES,
        default='other'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_case_notes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Case Note"
        verbose_name_plural = "Case Notes"

    def __str__(self):
        return f"Case Note for {self.client.full_name} - {self.get_interaction_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"

    def clean(self):
        """Validate that the caseworker creating the note is assigned to the client."""
        from django.core.exceptions import ValidationError
        
        if self.client and self.created_by:
            if self.client.assigned_caseworker != self.created_by:
                raise ValidationError(
                    "Only the assigned caseworker can create notes for this client."
                )
