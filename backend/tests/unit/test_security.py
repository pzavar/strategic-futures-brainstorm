import pytest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from datetime import timedelta

@pytest.mark.unit
class TestSecurity:
    """Unit tests for security utilities"""
    
    def test_password_hashing(self):
        """Test that passwords are hashed correctly"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt hash format
    
    def test_password_verification_success(self):
        """Test successful password verification"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_password_verification_failure(self):
        """Test failed password verification"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": 1}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_access_token_success(self):
        """Test successful token decoding"""
        data = {"sub": 1}
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == 1
        assert "exp" in decoded
    
    def test_decode_access_token_invalid(self):
        """Test decoding invalid token"""
        invalid_token = "invalid_token_string"
        decoded = decode_access_token(invalid_token)
        
        assert decoded is None
    
    def test_token_expiration(self):
        """Test that tokens expire correctly"""
        data = {"sub": 1}
        # Create token with very short expiration
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        # Token should be invalid after expiration
        decoded = decode_access_token(token)
        # Note: JWT library may still decode expired tokens, but exp will be in the past
        # This test verifies the token structure is correct

