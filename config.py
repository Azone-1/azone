"""
Configuration file for Azone Web App
Handles environment variables and app configuration
"""
import os

# Try to load environment variables from .env file if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional, continue without it
    pass

class Config:
    """Application configuration"""
    
    # Flask secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY',)
    
    # Database paths
    BOT_DB_PATH = os.getenv('BOT_DB_PATH', 'bots.db')
    SCHEDULED_POSTS_DB_PATH = os.getenv('SCHEDULED_POSTS_DB_PATH', 'web_scheduled_posts.db')
    
    # Server configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Domain configuration for webhooks and public URLs
    DOMAIN = os.getenv('DOMAIN', 'paing.xyz')  # Default: 'paing.xyz'
    USE_HTTPS = os.getenv('USE_HTTPS', 'True').lower() == 'true'  # Default to HTTPS for production

