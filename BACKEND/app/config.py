from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Your API Name"
    
    # Database Settings
    SUPABASE_URL: str | None = os.environ.get('SUPABASE_URL')
    SUPABASE_API: str | None = os.environ.get('SUPABASE_KEY')
    
    # CORS Settings
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Security Settings
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]


    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()


print(f"Loaded SUPABASE_URL: {settings.SUPABASE_URL}")
print(f"Loaded SUPABASE_API: {settings.SUPABASE_API}")