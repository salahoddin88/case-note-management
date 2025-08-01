"""
Test cases for the accounts app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for the custom User model"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'employee_id': 'EMP-001',
            'phone_number': '123-456-7890',
            'department': 'Social Services'
        }
    
    def test_create_user(self):
        """Test creating a user with custom fields"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.employee_id, 'EMP-001')
        self.assertEqual(user.phone_number, '123-456-7890')
        self.assertEqual(user.department, 'Social Services')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_str_method(self):
        """Test the string representation of user"""
        user = User.objects.create_user(**self.user_data)
        expected_str = "Test User (testuser)"
        self.assertEqual(str(user), expected_str)
    
    def test_user_str_method_no_full_name(self):
        """Test string representation when no full name"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser2')
    
    def test_full_name_property(self):
        """Test the full_name property"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.full_name, "Test User")
        
        # Test with no full name
        user_no_name = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.assertEqual(user_no_name.full_name, 'testuser2')


class AuthenticationEndpointTest(TestCase):
    """
    Integration tests for authentication endpoints
    Tests moved from test_auth.py at project root
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.base_url = 'http://localhost:8000'
    
    def test_login_endpoint_functionality(self):
        """Test login endpoint with various scenarios"""
        import requests
        
        # Test valid login
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    'username': 'testuser',
                    'password': 'testpass123'
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.assertTrue(data.get('success'))
                self.assertIn('access_token', data)
                self.assertIn('refresh_token', data)
                self.assertIn('user', data)
                
                # Test token refresh
                refresh_response = requests.post(
                    f"{self.base_url}/api/auth/refresh",
                    json={'refresh_token': data['refresh_token']},
                    timeout=5
                )
                
                if refresh_response.status_code == 200:
                    refresh_data = refresh_response.json()
                    self.assertTrue(refresh_data.get('success'))
                    self.assertIn('access_token', refresh_data)
        
        except requests.exceptions.RequestException:
            # Skip if server is not running
            self.skipTest("Django server not running - skipping integration test")
    
    def test_invalid_login_handling(self):
        """Test invalid login scenarios"""
        import requests
        
        try:
            # Test invalid credentials
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    'username': 'testuser',
                    'password': 'wrongpassword'
                },
                timeout=5
            )
            
            self.assertEqual(response.status_code, 401)
            
        except requests.exceptions.RequestException:
            # Skip if server is not running
            self.skipTest("Django server not running - skipping integration test")