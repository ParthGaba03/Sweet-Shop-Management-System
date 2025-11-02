from pydantic import BaseModel, EmailStr, Field, field_validator  # <-- Added 'field_validator'
from typing import Optional
from decimal import Decimal
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """
    This is the corrected UserCreate schema.
    We removed max_length from Field() and added a custom validator
    to check the BYTE length of the password.
    """
    password: str = Field(..., min_length=8) # <-- Removed max_length=72
    role: Optional[str] = Field(default="user", description="User role: 'user' or 'admin'. Admin has full management access.")

    @field_validator('password')
    @classmethod
    def validate_password_byte_length(cls, v: str) -> str:
        """Custom validator to check password byte length for bcrypt."""
        
        # Encode the password string into bytes (using UTF-8)
        password_bytes = v.encode('utf-8')
        
        # Check the length of the byte array
        if len(password_bytes) > 72:
            # This error will be caught by FastAPI and returned as a 422
            raise ValueError('Password cannot be more than 72 bytes.')
            
        # If valid, return the original password string
        return v
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate that role is either 'user' or 'admin'."""
        if v and v not in ['user', 'admin']:
            raise ValueError('Role must be either "user" or "admin"')
        return v or "user"

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenWithUser(Token):
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class PasswordResetResponse(BaseModel):
    message: str
    reset_token: Optional[str] = None  # For development/testing - remove in production

class SweetBase(BaseModel):
    name: str
    category: str
    price: Decimal
    quantity: int

class SweetCreate(SweetBase):
    pass

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None

class SweetResponse(SweetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PurchaseRequest(BaseModel):
    quantity: int = 1

class RestockRequest(BaseModel):
    quantity: int

class PurchaseHistoryResponse(BaseModel):
    id: int
    sweet_name: str
    category: str
    price: Decimal
    quantity: int
    total_price: Decimal
    purchased_at: datetime
    
    class Config:
        from_attributes = True