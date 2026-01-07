"""
Configuration settings for the FastAPI backend
"""
import sys
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Security
    # IMPORTANT: Set SECRET_KEY in .env file for production!
    # Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
    SECRET_KEY: str = "dev-secret-key-change-in-production-INSECURE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Testing - Set to False to disable authentication (ONLY FOR DEVELOPMENT!)
    ENABLE_AUTH: bool = False

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    INPUT_DIR: Path = BASE_DIR / "input"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    DATA_DIR: Path = BASE_DIR / "data"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/video_platform.db"

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://10.244.132.148:3000",  # ZeroTier server IP
        "http://10.244.51.225:3000",   # Mac ZeroTier IP
    ]

    # File Upload
    MAX_UPLOAD_SIZE: int = 5368709120  # 5GB in bytes

    class Config:
        env_file = ".env"


settings = Settings()

# Ensure directories exist
settings.INPUT_DIR.mkdir(exist_ok=True)
settings.OUTPUT_DIR.mkdir(exist_ok=True)
settings.DATA_DIR.mkdir(exist_ok=True)

# Security check for production
if settings.SECRET_KEY == "dev-secret-key-change-in-production-INSECURE":
    import os
    if os.getenv("ENVIRONMENT", "development").lower() == "production":
        print("=" * 80)
        print("CRITICAL SECURITY WARNING!")
        print("You are using the default SECRET_KEY in production!")
        print("Set a secure SECRET_KEY in your .env file immediately.")
        print("Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
        print("=" * 80)
        sys.exit(1)
    else:
        print("⚠️  Warning: Using default SECRET_KEY (development mode only)")
        print("   For production, set SECRET_KEY in .env file")
