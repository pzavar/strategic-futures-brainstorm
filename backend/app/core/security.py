from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid
import logging
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # bcrypt expects bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password with validation"""
    # Add validation BEFORE hashing
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(password) > 128:
        raise ValueError("Password too long")
    
    # Check for required character types
    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_number = any(c.isdigit() for c in password)
    
    if not has_uppercase:
        raise ValueError("Password must contain at least one uppercase letter")
    if not has_lowercase:
        raise ValueError("Password must contain at least one lowercase letter")
    if not has_number:
        raise ValueError("Password must contain at least one number")
    
    # Hash using bcrypt directly (more reliable than passlib with bcrypt 5.0.0)
    password_bytes = password.encode('utf-8')
    # Generate salt and hash (bcrypt automatically handles salt generation)
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),  # Issued at - CRITICAL for security
        "type": "access",  # Token type - prevents refresh token being used as access
        "jti": str(uuid.uuid4())  # JWT ID - enables revocation if needed later
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a refresh token (longer lived)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": str(uuid.uuid4())
    })
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True}  # Explicit expiry check
        )
        
        # Validate token type
        if payload.get("type") != "access":
            logger.warning("Invalid token type attempted")
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        logger.info("Expired token attempted")
        return None
    except jwt.JWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        return None


def decode_refresh_token(token: str) -> Optional[dict]:
    """Decode and verify a refresh token"""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True}
        )
        
        # Validate token type
        if payload.get("type") != "refresh":
            logger.warning("Invalid refresh token type attempted")
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        logger.info("Expired refresh token attempted")
        return None
    except jwt.JWTError as e:
        logger.warning(f"Invalid refresh token: {str(e)}")
        return None

