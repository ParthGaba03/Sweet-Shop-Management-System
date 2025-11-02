from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import decode_access_token

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    import sys
    print(f"🔍 get_current_user called - Starting authentication", flush=True)
    print(f"🔍 Credentials object: {credentials}", flush=True)
    
    if credentials is None:
        print("❌ No credentials provided", flush=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated - Authorization header missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"🔍 Credentials received, scheme: {credentials.scheme}, token: {credentials.credentials[:30]}...", flush=True)
    sys.stderr.write(f"🔍 get_current_user called - token received\n")
    
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        print("❌ Token decode failed", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        print("❌ Username not in token", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        print(f"❌ User not found in DB: {username}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Debug: log user info for admin checks
    print(f"✅ get_current_user: username={user.username}, role={user.role}", flush=True)
    sys.stderr.write(f"✅ get_current_user: username={user.username}, role={user.role}\n")
    
    return user

def require_admin(current_user: User = Depends(get_current_user)):
    # Debug: log the user info
    import sys
    print(f"🔍 require_admin check: user={current_user.username}, role={current_user.role}", flush=True)
    sys.stderr.write(f"🔍 require_admin check: user={current_user.username}, role={current_user.role}\n")
    
    # Check role from database (not from token)
    if current_user.role != "admin":
        print(f"❌ Admin check FAILED: role={current_user.role}, expected='admin'", flush=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Admin access required. Current role: {current_user.role}. Username: {current_user.username}"
        )
    print(f"✅ Admin check PASSED: user={current_user.username}", flush=True)
    return current_user

