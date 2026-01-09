from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "food_ordering_db"
    
    # Application settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        """Construct MySQL database URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Global settings instance
settings = Settings()
