# Generated by Django 5.2.4 on 2025-08-01 13:20

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseNote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(help_text='Detailed notes about the client interaction')),
                ('interaction_type', models.CharField(choices=[('phone', 'Phone Call'), ('in-person', 'In-Person Meeting'), ('email', 'Email'), ('video', 'Video Call'), ('other', 'Other')], default='other', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_notes', to='clients.client')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_case_notes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Case Note',
                'verbose_name_plural': 'Case Notes',
                'ordering': ['-created_at'],
            },
        ),
    ]
