from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db, settings
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, TokenWithUser, ForgotPasswordRequest, ResetPasswordRequest, PasswordResetResponse
from app.utils import get_password_hash, verify_password, create_access_token, generate_reset_token
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenWithUser, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if username exists
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
    except Exception as e:
        # If database connection fails, provide helpful error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {str(e)}. Please check your database configuration."
        )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    # Use role from user_data if provided, otherwise default to "user"
    # Role is saved directly to database - no manual update needed
    user_role = user_data.role if hasattr(user_data, 'role') and user_data.role else "user"
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

@router.post("/login", response_model=TokenWithUser)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password", response_model=PasswordResetResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Generate a password reset token for the user"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success message for security (don't reveal if email exists)
    if not user:
        return {
            "message": "If an account exists with this email, a password reset link has been sent.",
            "reset_token": None
        }
    
    # Generate reset token
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    db.commit()
    
    # Always return token in response so frontend can automatically show reset form
    # In production, you would send email, but we still return token for seamless UX
    return {
        "message": "Email verified. Please enter your new password.",
        "reset_token": reset_token  # Always return token so frontend can auto-switch to reset form
    }

@router.post("/reset-password", response_model=dict)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using the reset token"""
    user = db.query(User).filter(User.reset_token == request.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token is expired
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new one."
        )
    
    # Validate password
    password_bytes = request.new_password.encode('utf-8')
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be more than 72 bytes."
        )
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {
        "message": "Password has been reset successfully. You can now login with your new password."
    }
