# This file makes the 'core' directory a Python package.
# It allows you to import config and security settings directly from app.core

from .config import settings
from .security import verify_password, get_password_hash, create_access_token