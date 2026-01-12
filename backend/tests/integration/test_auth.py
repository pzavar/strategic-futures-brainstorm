import pytest
from faker import Faker

fake = Faker()

@pytest.mark.integration
class TestAuthEndpoints:
    """Integration tests for authentication endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        email = fake.email()
        password = "test_password_123"
        
        response = client.post(
            "/api/auth/register",
            json={"email": email, "password": password}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        email = fake.email()
        password = "test_password_123"
        
        # First registration
        client.post(
            "/api/auth/register",
            json={"email": email, "password": password}
        )
        
        # Second registration with same email
        response = client.post(
            "/api/auth/register",
            json={"email": email, "password": password}
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_login_success(self, client):
        """Test successful login"""
        email = fake.email()
        password = "test_password_123"
        
        # Register first
        client.post(
            "/api/auth/register",
            json={"email": email, "password": password}
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={"email": email, "password": password}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrong_password"}
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower() or "invalid" in response.json()["detail"].lower()

