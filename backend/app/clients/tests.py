"""
Test cases for the clients app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Client
import uuid

User = get_user_model()


class ClientModelTest(TestCase):
    """Test cases for the Client model"""
    
    def setUp(self):
        self.caseworker = User.objects.create_user(
            username='caseworker1',
            email='caseworker1@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        self.client_data = {
            'client_id': 'CL-2024-001',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'assigned_caseworker': self.caseworker
        }
    
    def test_create_client(self):
        """Test creating a client"""
        client = Client.objects.create(**self.client_data)
        
        self.assertEqual(client.client_id, 'CL-2024-001')
        self.assertEqual(client.first_name, 'Jane')
        self.assertEqual(client.last_name, 'Smith')
        self.assertEqual(client.assigned_caseworker, self.caseworker)
        self.assertIsInstance(client.id, uuid.UUID)
    
    def test_client_str_method(self):
        """Test the string representation of client"""
        client = Client.objects.create(**self.client_data)
        expected_str = "Jane Smith (CL-2024-001)"
        self.assertEqual(str(client), expected_str)
    
    def test_full_name_property(self):
        """Test the full_name property"""
        client = Client.objects.create(**self.client_data)
        self.assertEqual(client.full_name, "Jane Smith")
    
    def test_client_id_unique(self):
        """Test that client_id must be unique"""
        Client.objects.create(**self.client_data)
        
        # Try to create another client with the same client_id
        duplicate_data = self.client_data.copy()
        duplicate_data['first_name'] = 'Different'
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            Client.objects.create(**duplicate_data)
    
    def test_client_ordering(self):
        """Test that clients are ordered by creation date (newest first)"""
        client1 = Client.objects.create(
            client_id='CL-2024-001',
            first_name='First',
            last_name='Client',
            assigned_caseworker=self.caseworker
        )
        client2 = Client.objects.create(
            client_id='CL-2024-002',
            first_name='Second',
            last_name='Client',
            assigned_caseworker=self.caseworker
        )
        
        clients = list(Client.objects.all())
        self.assertEqual(clients[0], client2)  # Newest first
        self.assertEqual(clients[1], client1)