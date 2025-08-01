"""
Test cases for the case_notes app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from clients.models import Client
from .models import CaseNote
import uuid

User = get_user_model()


class CaseNoteModelTest(TestCase):
    """Test cases for the CaseNote model"""
    
    def setUp(self):
        self.caseworker = User.objects.create_user(
            username='caseworker1',
            email='caseworker1@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        self.other_caseworker = User.objects.create_user(
            username='caseworker2',
            email='caseworker2@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith'
        )
        
        self.client = Client.objects.create(
            client_id='CL-2024-001',
            first_name='Alice',
            last_name='Johnson',
            assigned_caseworker=self.caseworker
        )
        
        self.case_note_data = {
            'client': self.client,
            'content': 'Initial assessment completed. Client is cooperative.',
            'interaction_type': 'in-person',
            'created_by': self.caseworker
        }
    
    def test_create_case_note(self):
        """Test creating a case note"""
        case_note = CaseNote.objects.create(**self.case_note_data)
        
        self.assertEqual(case_note.client, self.client)
        self.assertEqual(case_note.content, 'Initial assessment completed. Client is cooperative.')
        self.assertEqual(case_note.interaction_type, 'in-person')
        self.assertEqual(case_note.created_by, self.caseworker)
        self.assertIsInstance(case_note.id, uuid.UUID)
    
    def test_case_note_str_method(self):
        """Test the string representation of case note"""
        case_note = CaseNote.objects.create(**self.case_note_data)
        expected_str = f"Case Note for Alice Johnson - In-Person Meeting ({case_note.created_at.strftime('%Y-%m-%d')})"
        self.assertEqual(str(case_note), expected_str)
    
    def test_interaction_type_choices(self):
        """Test that interaction type choices are enforced"""
        valid_types = ['phone', 'in-person', 'email', 'video', 'other']
        
        for interaction_type in valid_types:
            case_note_data = self.case_note_data.copy()
            case_note_data['interaction_type'] = interaction_type
            case_note = CaseNote.objects.create(**case_note_data)
            self.assertEqual(case_note.interaction_type, interaction_type)
    
    def test_case_note_ordering(self):
        """Test that case notes are ordered by creation date (newest first)"""
        note1 = CaseNote.objects.create(**self.case_note_data)
        
        note2_data = self.case_note_data.copy()
        note2_data['content'] = 'Follow-up meeting completed.'
        note2 = CaseNote.objects.create(**note2_data)
        
        notes = list(CaseNote.objects.all())
        self.assertEqual(notes[0], note2)  # Newest first
        self.assertEqual(notes[1], note1)
    
    def test_case_note_clean_method_valid(self):
        """Test that clean method allows assigned caseworker to create notes"""
        case_note = CaseNote(**self.case_note_data)
        # Should not raise any exception
        case_note.clean()
    
    def test_case_note_clean_method_invalid(self):
        """Test that clean method prevents unassigned caseworker from creating notes"""
        invalid_data = self.case_note_data.copy()
        invalid_data['created_by'] = self.other_caseworker
        
        case_note = CaseNote(**invalid_data)
        with self.assertRaises(ValidationError):
            case_note.clean()