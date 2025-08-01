import uuid
from django.db import models
from django.conf import settings


class Client(models.Model):
    """Model for storing client information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField(max_length=20, unique=True, help_text="Human-readable client ID (e.g., CL-2024-001)")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    assigned_caseworker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_clients'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.client_id})"

    @property
    def full_name(self):
        """Return the client's full name."""
        return f"{self.first_name} {self.last_name}"
