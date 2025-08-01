from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending AbstractUser for case note management system
    """
    # Additional fields for caseworkers
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True, 
                                 help_text="Employee ID for caseworkers")
    phone_number = models.CharField(max_length=15, blank=True, 
                                  help_text="Contact phone number")
    department = models.CharField(max_length=100, blank=True,
                                help_text="Department or team")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'auth_user'  # Keep the same table name for compatibility
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})" if self.get_full_name() else self.username
    
    @property
    def full_name(self):
        """Return full name or username if no full name available"""
        return self.get_full_name() or self.username