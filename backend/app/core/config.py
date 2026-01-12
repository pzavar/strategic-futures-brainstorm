from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env (like JWT_SECRET which we removed)
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()

