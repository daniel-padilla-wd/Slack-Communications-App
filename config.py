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
    SANDBOX_MODE = True
    IS_AWS_LAMBDA = (
        os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None or 
        os.getenv('AWS_EXECUTION_ENV') is not None
    )
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    
    # AWS Secrets Manager secret names
    AWS_BOT_TOKEN_SECRET = "aws-secret-name"
    AWS_SIGNING_SECRET_SECRET = "aws-secret-name"
    
    @classmethod
    def get_bot_token(cls):
        """Get bot token based on environment."""
        if not cls.SANDBOX_MODE and cls.IS_AWS_LAMBDA:
            logging.info("Retrieving BOT_TOKEN from AWS Secrets Manager.")
            return get_secret_string(cls.AWS_BOT_TOKEN_SECRET)
        logging.info("Using BOT_TOKEN from environment variable.")
        return os.getenv("S_BOT_TOKEN")
    
    @classmethod
    def get_signing_secret(cls):
        """Get signing secret based on environment."""
        if not cls.SANDBOX_MODE and cls.IS_AWS_LAMBDA:
            logging.info("Retrieving SIGNING_SECRET from AWS Secrets Manager.")
            return get_secret_string(cls.AWS_SIGNING_SECRET_SECRET)
        logging.info("Using SIGNING_SECRET from environment variable.")
        return os.getenv("SIGNING_SECRET")
    
    @classmethod
    def get_app_token(cls):
        """Get app token for Socket Mode (local development only)."""
        if cls.SANDBOX_MODE or not cls.IS_AWS_LAMBDA:
            logging.info("Using S_APP_TOKEN for Socket Mode in sandbox/local development.")
            return os.getenv("S_APP_TOKEN")
        logging.info("APP_TOKEN not required in production/Lambda environment.")
        return None
    
    @classmethod
    def get_ssl_context(cls):
        """
        Create a custom SSL context for sandbox development only.
        Production/Lambda uses default SSL context.
        
        Returns:
            ssl.SSLContext or None: Custom SSL context for sandbox, None for production
        """
        if cls.SANDBOX_MODE:
            ca_file_path = certifi.where()
            context = ssl.create_default_context(cafile=ca_file_path)
            context.verify_flags &= ~ssl.VERIFY_X509_STRICT
            logging.info("Custom SSL context created for sandbox development.")
            return context
        logging.info("Using default SSL context for production/Lambda.")
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
        if not cls.SANDBOX_MODE and not signing_secret:
            raise ValueError("SIGNING_SECRET is required but not configured")
        
        # App token only required in sandbox mode
        if cls.SANDBOX_MODE and not cls.get_app_token():
            raise ValueError("S_APP_TOKEN is required for Socket Mode in sandbox")
        
        return True

# Initialize tokens and context at module level
BOT_TOKEN = Config.get_bot_token()
SIGNING_SECRET = Config.get_signing_secret()
APP_TOKEN = Config.get_app_token()
SSL_CONTEXT = Config.get_ssl_context()
