import os
import logging
from dotenv import load_dotenv
from aws_secrets import get_secret_string
import ssl
import certifi

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for managing environment variables and settings."""
    
    # Environment detection
    PRODUCTION = False
    SIGNING_SECRET = os.getenv("SIGNING_SECRET")
    S_BOT_TOKEN = os.getenv("S_BOT_TOKEN")
    S_APP_TOKEN = os.getenv("S_APP_TOKEN")

    
    # Logging configuration
    LOG_LEVEL = 'DEBUG'
    
    # AWS Secrets Manager secret names
    AWS_BOT_TOKEN_SECRET = "bot_token_secret_name"
    AWS_SIGNING_SECRET_SECRET = "signing_secret_name"
    
    @classmethod
    def get_bot_token(cls):
        """Get bot token based on environment."""
        if not cls.PRODUCTION:
            return cls.S_BOT_TOKEN
        return get_secret_string(cls.AWS_BOT_TOKEN_SECRET)
    
    @classmethod
    def get_signing_secret(cls):
        """Get signing secret based on environment."""
        if not cls.PRODUCTION:
            return cls.SIGNING_SECRET
        return get_secret_string(cls.AWS_SIGNING_SECRET_SECRET)
    
    @classmethod
    def get_app_token(cls):
        """Get app token for Socket Mode (local development only)."""
        if not cls.PRODUCTION:
            return cls.S_APP_TOKEN
        return None
    
    @classmethod
    def get_ssl_context(cls):
        """
        Create a custom SSL context for sandbox development only.
        Production uses default SSL context.
        
        Returns:
            ssl.SSLContext or None: Custom SSL context for sandbox, None for production
        """
        if not cls.PRODUCTION:
            ca_file_path = certifi.where()
            context = ssl.create_default_context(cafile=ca_file_path)
            context.verify_flags &= ~ssl.VERIFY_X509_STRICT
            return context
        return None
    
    @classmethod
    def setup_logging(cls):
        """Configure logging for the application."""
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=getattr(logging, cls.LOG_LEVEL)
        )
    
    @classmethod
    def validate(cls):
        """
        Validate that required configuration is present.
        
        Raises:
            ValueError: If required configuration is missing
        """
        bot_token = cls.get_bot_token()
        signing_secret = cls.get_signing_secret()
        
        if not bot_token:
            raise ValueError("BOT_TOKEN is required but not configured")
        if not cls.PRODUCTION and not signing_secret:
            raise ValueError("SIGNING_SECRET is required but not configured")
        
        # App token only required in sandbox mode
        if cls.PRODUCTION and not cls.get_app_token():
            raise ValueError("S_APP_TOKEN is required for Socket Mode in sandbox")
        
        return True

# Initialize tokens and context at module level
BOT_TOKEN = Config.get_bot_token()
SIGNING_SECRET = Config.get_signing_secret()
APP_TOKEN = Config.get_app_token()
SSL_CONTEXT = Config.get_ssl_context()
