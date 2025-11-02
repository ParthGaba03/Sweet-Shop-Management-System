import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, sweets

app = FastAPI(title="Sweet Shop Management System API", version="1.0.0", redirect_slashes=False)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log incoming requests for debugging
    auth_header = request.headers.get("Authorization")
    print(f"📥 {request.method} {request.url.path} - Auth header: {'Present' if auth_header else 'MISSING'} - {auth_header[:30] if auth_header else ''}...", flush=True)
    response = await call_next(request)
    return response

# CORS middleware
# Get allowed origins from environment variable (comma-separated) or use default
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Supports multiple origins (dev + production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],  # Explicitly allow Authorization header
    expose_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(sweets.router, prefix="/api/sweets", tags=["sweets"])

@app.on_event("startup")
async def startup_event():
    """Create database tables and run migrations on startup"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified successfully")
        
        # Run migration for password reset fields (safe migration - won't fail if columns exist)
        from sqlalchemy import text, inspect
        inspector = inspect(engine)
        
        # Check if users table exists and has reset_token column
        if inspector.has_table("users"):
            columns = [col['name'] for col in inspector.get_columns("users")]
            
            # Add reset_token column if it doesn't exist
            if 'reset_token' not in columns:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN reset_token VARCHAR"))
                    print("✅ Added reset_token column to users table")
            
            # Add reset_token_expires column if it doesn't exist
            if 'reset_token_expires' not in columns:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP WITH TIME ZONE"))
                    print("✅ Added reset_token_expires column to users table")
            
            # Create index if it doesn't exist
            indexes = [idx['name'] for idx in inspector.get_indexes("users")]
            if 'idx_users_reset_token' not in indexes:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("CREATE INDEX idx_users_reset_token ON users(reset_token)"))
                        print("✅ Created index on reset_token")
                except Exception as e:
                    print(f"⚠️ Index may already exist: {e}")
            
            print("✅ Password reset migration completed")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not create tables/migrations on startup: {e}")
        print("Tables will be created on first database access")

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
