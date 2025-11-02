from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
import sys
import os
from pathlib import Path
from dotenv import load_dotenv  # We still need this for the other keys

# --- Configuration ---

current_file_dir = Path(__file__).parent
base_dir = current_file_dir.parent
env_file_path = base_dir / ".env"

# --- Manually load the .env file ---
# This will load SECRET_KEY, ALGORITHM, etc.
# It will (and is) failing on DATABASE_URL, which is fine now.
if env_file_path.exists():
    load_dotenv(dotenv_path=env_file_path, override=True)
else:
    sys.stderr.write(f"⚠️ WARNING: .env file not found at {env_file_path}\n")
# ---

class Settings(BaseSettings):
    """
    Settings class for application configuration.
    All variables can be loaded from environment variables or .env file.
    """
    
    # DATABASE_URL from environment variable (priority) or .env file or default for local dev
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Gunnu%400301@localhost:5432/sweet_shop_db")
    
    # These will be loaded from environment or .env file (with defaults if not found)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    DEBUG: bool = False
    
    model_config = SettingsConfigDict(
        case_sensitive=False,  # Allow lowercase access
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra fields from .env
    )

# Create the settings instance.
try:
    settings = Settings()
except Exception as e:
    # This error should now be fixed, but we leave the check.
    sys.stderr.write(f"⚠️ CRITICAL: Could not validate settings.\n")
    sys.stderr.write(f"⚠️ Make sure your .env file has SECRET_KEY, ALGORITHM, etc. Error: {e}\n")
    sys.exit(1) # Exit if settings can't be loaded

# Debug: print what URL we're using
if settings.DATABASE_URL:
    try:
        safe_url = settings.DATABASE_URL.split("@")[0] + "@***"
        sys.stderr.write(f"✅ Settings validated. Using DB: {safe_url}...\n")
    except Exception:
        pass

# --- Database Setup ---

engine = create_engine(
    settings.DATABASE_URL, # This will use the hardcoded URL
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Dependency ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()