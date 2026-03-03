import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True
    )
    
    project_name: str = "Crop Assistant AI"
    project_version: str = "1.0.0"
    debug: bool = True
    
    # API Settings
    api_v1_str: str = "/api/v1"
    
    # Database - Use lowercase to match pydantic_settings behavior
    database_url: str = "postgresql://user:password@db:5432/cropdb"
    mongodb_url: str = "mongodb://root:password@mongodb:27017/cropdb"
    
    # Security
    secret_key: str = "your-secret-key-change-in-prod"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # ML Model Paths
    disease_model_path: str = "./ml/models/disease_model.h5"
    groundwater_model_path: str = "./ml/models/groundwater_model.pkl"
    production_model_path: str = "./ml/models/production_model.pkl"
    
    # LLM Settings
    use_local_llm: bool = True
    llm_api_key: str = ""
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return self.database_url
    
    @property
    def PROJECT_NAME(self) -> str:
        return self.project_name
    
    @property
    def PROJECT_VERSION(self) -> str:
        return self.project_version
    
    @property
    def DEBUG(self) -> bool:
        return self.debug

settings = Settings()
