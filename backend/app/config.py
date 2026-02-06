"""
Configuration settings for the RAG chatbot
Loads from environment variables
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
  
    OPENAI_API_KEY: str
    
  
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    
  
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
 
    CORS_ORIGINS: list = [
        "http://localhost:5173",  
        "http://localhost:3000",  
    ]
    
 
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVAL_TOP_K: int = 5
    
   
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True



settings = Settings()

