import os
import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Initialize security scheme
security = HTTPBearer()

print(f"SECRET_KEY loaded: {'Yes' if SECRET_KEY != 'your_secret_key_here' else 'No'}")
print(f"ALGORITHM: {ALGORITHM}, EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT token with expiration and additional security claims"""
    to_encode = data.copy()
    
    # Set expiration time
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    # Add claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(UTC),  # issued at
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify JWT token with proper error handling"""
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            options={
                "verify_exp": True,  # Verify expiration
                "verify_iat": True,  # Verify issued at time
            }
        )
        return payload
    except JWTError as e:
        print(f"Token verification error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during token verification: {e}")
        return None

def get_current_user_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user payload from JWT token with proper HTTP exception handling"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    token_type: str = payload.get("type")
    
    if username is None:
        raise credentials_exception
    
    if token_type != "access":
        raise credentials_exception
    
    return payload

def get_current_user_username(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract username from token (for backward compatibility)"""
    payload = get_current_user_payload(credentials)
    username = payload.get("sub")
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return username

def _truncate_password_bytes(password: str) -> bytes:
    """
    Truncate password bytes to 72 bytes for bcrypt compatibility.
    Note: This is a security trade-off for bcrypt limitations.
    Consider using argon2 instead for better security with longer passwords.
    """
    pw_bytes = password.encode("utf-8")
    if len(pw_bytes) > 72:
        print(f"Warning: Password truncated from {len(pw_bytes)} to 72 bytes for bcrypt compatibility")
        return pw_bytes[:72]
    return pw_bytes

def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for password"""
    pw_bytes = _truncate_password_bytes(password)
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt(rounds=12))  # Increased rounds for security
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password"""
    try:
        pw_bytes = _truncate_password_bytes(plain_password)
        return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))
    except (ValueError, TypeError) as e:
        print(f"Password verification error: {e}")
        return False

# Optional: Add refresh token functionality
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a refresh token with longer expiration"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=7))  # 7 days for refresh token
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(UTC),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt