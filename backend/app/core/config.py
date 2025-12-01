import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "EMS System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database Settings
    # Defaults to localhost if not found in .env
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/ems_db")
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_to_a_secure_random_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Initialize settings
settings = Settings()