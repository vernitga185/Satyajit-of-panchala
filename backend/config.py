import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    FINAL_FLAG: str = os.environ.get("FINAL_FLAG", "FLAG{s4ty4j1t_0f_p4nch4l4_unl0ck3d}")
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "http://localhost:8000")
    SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "dummy")
    TOGETHER_API_KEY: str = os.environ.get("TOGETHER_API_KEY", "dummy")
    MODEL_NAME: str = "Qwen/Qwen2.5-72B-Instruct" # Using closest available for Qwen3-8B

settings = Settings()
