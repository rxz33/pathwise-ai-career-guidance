from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load env file
load_dotenv()

# Get encryption key from .env
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not found in .env file")

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """Encrypt sensitive string data."""
    if data is None:
        return None
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    """Decrypt sensitive string data."""
    if data is None:
        return None
    return fernet.decrypt(data.encode()).decode()
