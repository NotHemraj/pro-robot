import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Main configuration class for the bot"""
    
    # ====== BOT CONFIGURATION ======
    TOKEN = os.getenv('BOT_TOKEN')
    BOT_USERNAME = os.getenv('BOT_USERNAME', '@YourBot')
    BOT_NAME = os.getenv('BOT_NAME', 'Advanced Telegram Bot')
    BOT_VERSION = os.getenv('BOT_VERSION', '2.0.0')
    
    # ====== DATABASE CONFIGURATION ======
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/bot.db')
    DATABASE_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', '10'))
    DATABASE_MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', '20'))
    DATABASE_POOL_TIMEOUT = int(os.getenv('DATABASE_POOL_TIMEOUT', '30'))
    DATABASE_POOL_RECYCLE = int(os.getenv('DATABASE_POOL_RECYCLE', '3600'))
    
    # ====== REDIS CONFIGURATION ======
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_SOCKET_TIMEOUT = int(os.getenv('REDIS_SOCKET_TIMEOUT', '5'))
    REDIS_CONNECTION_POOL_MAX = int(os.getenv('REDIS_CONNECTION_POOL_MAX', '50'))
    
    # ====== LOGGING CONFIGURATION ======
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
    LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', '10485760'))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
    LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%d %H:%M:%S')
    ENABLE_FILE_LOGGING = os.getenv('ENABLE_FILE_LOGGING', 'true').lower() == 'true'
    ENABLE_CONSOLE_LOGGING = os.getenv('ENABLE_CONSOLE_LOGGING', 'true').lower() == 'true'
    
    # ====== SECURITY CONFIGURATION ======
    RATE_LIMIT_PER_USER = int(os.getenv('RATE_LIMIT_PER_USER', '5'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    
    # Global rate limits
    GLOBAL_RATE_LIMIT_ENABLED = os.getenv('GLOBAL_RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    GLOBAL_RATE_LIMIT_PER_SECOND = int(os.getenv('GLOBAL_RATE_LIMIT_PER_SECOND', '30'))
    GLOBAL_RATE_LIMIT_BURST = int(os.getenv('GLOBAL_RATE_LIMIT_BURST', '10'))
    
    # Security features
    ENABLE_SECURITY_LOGS = os.getenv('ENABLE_SECURITY_LOGS', 'true').lower() == 'true'
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4096'))
    MAX_CAPTION_LENGTH = int(os.getenv('MAX_CAPTION_LENGTH', '1024'))
    
    # ====== ADMIN CONFIGURATION ======
    SUDO_USERS = []
    SUPPORT_USERS = []
    WHITELIST_USERS = []
    BLACKLIST_USERS = []
    
    # Parse user lists from environment
    if os.getenv('SUDO_USERS'):
        try:
            SUDO_USERS = [int(x.strip()) for x in os.getenv('SUDO_USERS').split(',') if x.strip()]
        except ValueError:
            SUDO_USERS = []
    
    if os.getenv('SUPPORT_USERS'):
        try:
            SUPPORT_USERS = [int(x.strip()) for x in os.getenv('SUPPORT_USERS').split(',') if x.strip()]
        except ValueError:
            SUPPORT_USERS = []
    
    if os.getenv('WHITELIST_USERS'):
        try:
            WHITELIST_USERS = [int(x.strip()) for x in os.getenv('WHITELIST_USERS').split(',') if x.strip()]
        except ValueError:
            WHITELIST_USERS = []
    
    if os.getenv('BLACKLIST_USERS'):
        try:
            BLACKLIST_USERS = [int(x.strip()) for x in os.getenv('BLACKLIST_USERS').split(',') if x.strip()]

except ValueError:
            BLACKLIST_USERS = []
    
    # ====== FEATURE FLAGS ======
    ENABLE_ANTIFLOOD = os.getenv('ENABLE_ANTIFLOOD', 'true').lower() == 'true'
    ENABLE_ANTIRAID = os.getenv('ENABLE_ANTIRAID', 'true').lower() == 'true'
    ENABLE_CAPTCHA = os.getenv('ENABLE_CAPTCHA', 'true').lower() == 'true'
    ENABLE_FILTERS = os.getenv('ENABLE_FILTERS', 'true').lower() == 'true'
    ENABLE_NOTES = os.getenv('ENABLE_NOTES', 'true').lower() == 'true'
    ENABLE_RULES = os.getenv('ENABLE_RULES', 'true').lower() == 'true'
    ENABLE_WARNS = os.getenv('ENABLE_WARNS', 'true').lower() == 'true'
    ENABLE_BANS = os.getenv('ENABLE_BANS', 'true').lower() == 'true'
    ENABLE_LOCKS = os.getenv('ENABLE_LOCKS', 'true').lower() == 'true'
    ENABLE_APPROVAL = os.getenv('ENABLE_APPROVAL', 'true').lower() == 'true'
    ENABLE_BLACKLISTS = os.getenv('ENABLE_BLACKLISTS', 'true').lower() == 'true'
    ENABLE_FEDERATIONS = os.getenv('ENABLE_FEDERATIONS', 'true').lower() == 'true'
    ENABLE_CONNECTIONS = os.getenv('ENABLE_CONNECTIONS', 'true').lower() == 'true'
    ENABLE_GREETINGS = os.getenv('ENABLE_GREETINGS', 'true').lower() == 'true'
    ENABLE_LOGS = os.getenv('ENABLE_LOGS', 'true').lower() == 'true'
    ENABLE_REPORTS = os.getenv('ENABLE_REPORTS', 'true').lower() == 'true'
    ENABLE_PURGES = os.getenv('ENABLE_PURGES', 'true').lower() == 'true'
    ENABLE_PIN = os.getenv('ENABLE_PIN', 'true').lower() == 'true'
    ENABLE_TOPICS = os.getenv('ENABLE_TOPICS', 'true').lower() == 'true'
    ENABLE_PRIVACY = os.getenv('ENABLE_PRIVACY', 'true').lower() == 'true'
    ENABLE_LANGUAGES = os.getenv('ENABLE_LANGUAGES', 'true').lower() == 'true'
    ENABLE_IMPORT_EXPORT = os.getenv('ENABLE_IMPORT_EXPORT', 'true').lower() == 'true'
    ENABLE_CLEAN_SERVICE = os.getenv('ENABLE_CLEAN_SERVICE', 'true').lower() == 'true'
    ENABLE_FORMATTING = os.getenv('ENABLE_FORMATTING', 'true').lower() == 'true'
    ENABLE_MISC = os.getenv('ENABLE_MISC', 'true').lower() == 'true'
    
    # ====== API KEYS ======
    PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
    TRANSLATE_API_KEY = os.getenv('TRANSLATE_API_KEY')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    TIMEZONE_API_KEY = os.getenv('TIMEZONE_API_KEY')
    REVERSE_SEARCH_API_KEY = os.getenv('REVERSE_SEARCH_API_KEY')
    PASTE_SERVICE_API_KEY = os.getenv('PASTE_SERVICE_API_KEY')
    
    # ====== WEBHOOK CONFIGURATION ======
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))
    WEBHOOK_LISTEN = os.getenv('WEBHOOK_LISTEN', '0.0.0.0')
    WEBHOOK_SSL_CERT = os.getenv('WEBHOOK_SSL_CERT')
    WEBHOOK_SSL_PRIV = os.getenv('WEBHOOK_SSL_PRIV')
    
    # ====== DEFAULT SETTINGS ======
    DEFAULT_WARN_LIMIT = int(os.getenv('DEFAULT_WARN_LIMIT', '3'))
    DEFAULT_WARN_ACTION = os.getenv('DEFAULT_WARN_ACTION', 'kick')
    DEFAULT_FLOOD_LIMIT = int(os.getenv('DEFAULT_FLOOD_LIMIT', '5'))
    DEFAULT_FLOOD_TIME = int(os.getenv('DEFAULT_FLOOD_TIME', '10'))
    DEFAULT_RAID_LIMIT = int(os.getenv('DEFAULT_RAID_LIMIT', '10'))
    DEFAULT_RAID_TIME = int(os.getenv('DEFAULT_RAID_TIME', '60'))
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    
    # Chat settings
    AUTO_DELETE_COMMANDS = os.getenv('AUTO_DELETE_COMMANDS', 'false').lower() == 'true'
    LOG_ALL_COMMANDS = os.getenv('LOG_ALL_COMMANDS', 'true').lower() == 'true'
    CLEAN_SERVICE_MESSAGES = os.getenv('CLEAN_SERVICE_MESSAGES', 'true').lower() == 'true'
    
    # ====== FILE HANDLING ======
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '52428800'))  # 50MB
    MAX_PHOTO_SIZE = int(os.getenv('MAX_PHOTO_SIZE', '10485760'))  # 10MB
    MAX_VIDEO_SIZE = int(os.getenv('MAX_VIDEO_SIZE', '52428800'))  # 50MB

MAX_AUDIO_SIZE = int(os.getenv('MAX_AUDIO_SIZE', '52428800'))  # 50MB
    MAX_VOICE_SIZE = int(os.getenv('MAX_VOICE_SIZE', '20971520'))  # 20MB
    MAX_DOCUMENT_SIZE = int(os.getenv('MAX_DOCUMENT_SIZE', '52428800'))  # 50MB
    
    ALLOWED_FILE_TYPES = os.getenv('ALLOWED_FILE_TYPES', 
        'jpg,jpeg,png,gif,bmp,webp,mp4,avi,mkv,mov,mp3,wav,ogg,flac,pdf,txt,doc,docx,zip,rar'
    ).split(',')
    
    # Upload directories
    UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
    TEMP_DIR = os.getenv('TEMP_DIR', 'temp')
    BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
    
    # ====== CACHE SETTINGS ======
    CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # 1 hour
    USER_CACHE_TTL = int(os.getenv('USER_CACHE_TTL', '1800'))  # 30 minutes
    CHAT_CACHE_TTL = int(os.getenv('CHAT_CACHE_TTL', '1800'))  # 30 minutes
    ADMIN_CACHE_TTL = int(os.getenv('ADMIN_CACHE_TTL', '300'))  # 5 minutes
    
    # ====== PERFORMANCE SETTINGS ======
    MAX_CONCURRENT_UPDATES = int(os.getenv('MAX_CONCURRENT_UPDATES', '256'))
    CONNECTION_POOL_SIZE = int(os.getenv('CONNECTION_POOL_SIZE', '8'))
    READ_TIMEOUT = int(os.getenv('READ_TIMEOUT', '6'))
    WRITE_TIMEOUT = int(os.getenv('WRITE_TIMEOUT', '7'))
    CONNECT_TIMEOUT = int(os.getenv('CONNECT_TIMEOUT', '7'))
    POOL_TIMEOUT = int(os.getenv('POOL_TIMEOUT', '1'))
    
    # ====== MONITORING SETTINGS ======
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    METRICS_PORT = int(os.getenv('METRICS_PORT', '8080'))
    ENABLE_HEALTH_CHECK = os.getenv('ENABLE_HEALTH_CHECK', 'true').lower() == 'true'
    HEALTH_CHECK_PORT = int(os.getenv('HEALTH_CHECK_PORT', '8081'))
    
    # Statistics collection
    COLLECT_STATS = os.getenv('COLLECT_STATS', 'true').lower() == 'true'
    STATS_RETENTION_DAYS = int(os.getenv('STATS_RETENTION_DAYS', '30'))
    
    # ====== BACKUP SETTINGS ======
    AUTO_BACKUP = os.getenv('AUTO_BACKUP', 'true').lower() == 'true'
    BACKUP_INTERVAL_HOURS = int(os.getenv('BACKUP_INTERVAL_HOURS', '24'))
    MAX_BACKUP_FILES = int(os.getenv('MAX_BACKUP_FILES', '7'))
    BACKUP_ENCRYPTION = os.getenv('BACKUP_ENCRYPTION', 'false').lower() == 'true'
    BACKUP_ENCRYPTION_KEY = os.getenv('BACKUP_ENCRYPTION_KEY')
    
    # ====== DEVELOPMENT SETTINGS ======
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    TESTING = os.getenv('TESTING', 'false').lower() == 'true'
    DEV_MODE = os.getenv('DEV_MODE', 'false').lower() == 'true'
    ENABLE_PROFILING = os.getenv('ENABLE_PROFILING', 'false').lower() == 'true'
    
    # ====== LOCALIZATION ======
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'en,hi,es,fr,de,ru,ar,zh').split(',')
    FALLBACK_LANGUAGE = os.getenv('FALLBACK_LANGUAGE', 'en')
    
    # ====== EXTERNAL SERVICES ======
    PASTE_SERVICE_URL = os.getenv('PASTE_SERVICE_URL', 'https://paste.ee')
    REVERSE_SEARCH_URL = os.getenv('REVERSE_SEARCH_URL', 'https://www.google.com/searchbyimage')
    WEATHER_SERVICE_URL = os.getenv('WEATHER_SERVICE_URL', 'https://api.openweathermap.org/data/2.5')
    TRANSLATE_SERVICE_URL = os.getenv('TRANSLATE_SERVICE_URL', 'https://api.mymemory.translated.net')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration and check required settings"""
        errors = []
        
        # Check required settings
        if not cls.TOKEN:
            errors.append("BOT_TOKEN is required")
        
        # Validate bot token format
        if cls.TOKEN and (':' not in cls.TOKEN or len(cls.TOKEN.split(':')) != 2):
            errors.append("BOT_TOKEN format is invalid")
        
        # Validate database URL
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is required")
        
        # Validate numeric settings
        numeric_settings = [

('RATE_LIMIT_PER_USER', cls.RATE_LIMIT_PER_USER, 1, 100),
            ('RATE_LIMIT_WINDOW', cls.RATE_LIMIT_WINDOW, 1, 3600),
            ('DEFAULT_WARN_LIMIT', cls.DEFAULT_WARN_LIMIT, 1, 20),
            ('DEFAULT_FLOOD_LIMIT', cls.DEFAULT_FLOOD_LIMIT, 1, 100),
            ('DEFAULT_FLOOD_TIME', cls.DEFAULT_FLOOD_TIME, 1, 300),
            ('DEFAULT_RAID_LIMIT', cls.DEFAULT_RAID_LIMIT, 1, 100),
            ('DEFAULT_RAID_TIME', cls.DEFAULT_RAID_TIME, 1, 3600),
        ]
        
        for setting_name, value, min_val, max_val in numeric_settings:
            if not min_val <= value <= max_val:
                errors.append(f"{setting_name} must be between {min_val} and {max_val}")
        
        # Validate warn action
        valid_warn_actions = ['kick', 'ban', 'mute', 'nothing']
        if cls.DEFAULT_WARN_ACTION not in valid_warn_actions:
            errors.append(f"DEFAULT_WARN_ACTION must be one of: {', '.join(valid_warn_actions)}")
        
        # Validate language
        if cls.DEFAULT_LANGUAGE not in cls.SUPPORTED_LANGUAGES:
            errors.append(f"DEFAULT_LANGUAGE must be one of: {', '.join(cls.SUPPORTED_LANGUAGES)}")
        
        # Validate webhook settings if enabled
        if cls.USE_WEBHOOK:
            if not cls.WEBHOOK_URL:
                errors.append("WEBHOOK_URL is required when USE_WEBHOOK is enabled")
            if not 1 <= cls.WEBHOOK_PORT <= 65535:
                errors.append("WEBHOOK_PORT must be between 1 and 65535")
        
        # Log errors and return result
        if errors:
            from helpers.logger import get_logger
            logger = get_logger(name)
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def load_from_file(cls, config_file: str) -> None:
        """Load configuration from JSON file"""
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Update class attributes
                for key, value in config_data.items():
                    if hasattr(cls, key):
                        setattr(cls, key, value)
                        
        except Exception as e:
            from helpers.logger import get_logger
            logger = get_logger(name)
            logger.error(f"Failed to load config from file {config_file}: {e}")
    
    @classmethod
    def save_to_file(cls, config_file: str) -> None:
        """Save current configuration to JSON file"""
        try:
            config_data = {}
            
            # Get all class attributes that are configuration values
            for attr in dir(cls):
                if not attr.startswith('_') and not callable(getattr(cls, attr)):
                    value = getattr(cls, attr)
                    if isinstance(value, (str, int, float, bool, list, dict)):
                        config_data[attr] = value
            
            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            from helpers.logger import get_logger
            logger = get_logger(name)
            logger.error(f"Failed to save config to file {config_file}: {e}")
    
    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """Get configuration summary for logging"""
        return {
            'bot_name': cls.BOT_NAME,

'bot_version': cls.BOT_VERSION,
            'database_type': cls.DATABASE_URL.split('://')[0] if cls.DATABASE_URL else 'unknown',
            'redis_enabled': bool(cls.REDIS_URL),
            'webhook_enabled': cls.USE_WEBHOOK,
            'debug_mode': cls.DEBUG,
            'enabled_features': sum([
                cls.ENABLE_ANTIFLOOD, cls.ENABLE_ANTIRAID, cls.ENABLE_CAPTCHA,
                cls.ENABLE_FILTERS, cls.ENABLE_NOTES, cls.ENABLE_RULES,
                cls.ENABLE_WARNS, cls.ENABLE_BANS, cls.ENABLE_LOCKS,
                cls.ENABLE_APPROVAL, cls.ENABLE_BLACKLISTS, cls.ENABLE_FEDERATIONS,
                cls.ENABLE_CONNECTIONS, cls.ENABLE_GREETINGS, cls.ENABLE_LOGS,
                cls.ENABLE_REPORTS, cls.ENABLE_PURGES, cls.ENABLE_PIN,
                cls.ENABLE_TOPICS, cls.ENABLE_PRIVACY, cls.ENABLE_LANGUAGES,
                cls.ENABLE_IMPORT_EXPORT, cls.ENABLE_CLEAN_SERVICE,
                cls.ENABLE_FORMATTING, cls.ENABLE_MISC
            ]),
            'sudo_users_count': len(cls.SUDO_USERS),
            'support_users_count': len(cls.SUPPORT_USERS),
            'supported_languages': len(cls.SUPPORTED_LANGUAGES)
        }

# Create directories if they don't exist
for directory in [Config.UPLOAD_DIR, Config.TEMP_DIR, Config.BACKUP_DIR, 'logs', 'data']:
    Path(directory).mkdir(parents=True, exist_ok=True)

# Export commonly used settings
TOKEN = Config.TOKEN
DATABASE_URL = Config.DATABASE_URL
REDIS_URL = Config.REDIS_URL
SUDO_USERS = Config.SUDO_USERS
SUPPORT_USERS = Config.SUPPORT_USERS
