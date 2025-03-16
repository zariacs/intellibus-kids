from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "NUTRI LAB"

    CLERK_API_KEY: str | None = os.environ.get('CLERK_API_KEY')
    
    NEVIN: str = os.environ.get('NEVIN')

    # Database Settings
    SUPABASE_URL: str | None = os.environ.get('SUPABASE_URL')
    SUPABASE_API: str | None = os.environ.get('SUPABASE_KEY')
    
    #YES WE KNOW THIS IS BAD, BUT WE ARE USING RENDER AND IT IS NOT ALLOWING US TO SET THE ORIGINS
    #CORS Settings - Allow all origins
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Security Settings - Allow all hosts
    ALLOWED_HOSTS: List[str] = ["*"]



    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
