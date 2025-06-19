#main randi rona
import asyncio
import sys
import signal
import os
from datetime import datetime
from bot import bot
from helpers.logger import get_logger
from config import Config
from database.models import init_db, close_db
import psutil

logger = get_logger(name)

class BotManager:
    def init(self):
        self.bot = bot
        self.start_time = datetime.now()
        self.is_running = False
        
    async def initialize(self):
        """Initialize all bot components"""
        try:
            logger.info("🔧 Initializing bot components...")
            
            # Validate configuration
            logger.info("📋 Validating configuration...")
            Config.validate()
            logger.info("✅ Configuration validated successfully")
            
            # Initialize database
            logger.info("🗄️ Initializing database...")
            await init_db()
            logger.info("✅ Database initialized successfully")
            
            # Setup bot
            logger.info("🤖 Setting up bot...")
            await self.bot.setup()
            logger.info("✅ Bot setup completed")
            
            # Log system information
            await self.log_system_info()
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize bot: {e}")
            raise
    
    async def log_system_info(self):
        """Log system and bot information"""
        try:
            # Get bot info
            bot_info = await self.bot.application.bot.get_me()
            
            # System info
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            logger.info("📊 System Information:")
            logger.info(f"   Bot: @{bot_info.username} ({bot_info.first_name})")
            logger.info(f"   Bot ID: {bot_info.id}")
            logger.info(f"   Python: {sys.version}")
            logger.info(f"   Platform: {sys.platform}")
            logger.info(f"   Memory: {memory.percent}% used ({memory.available // 1024 // 1024} MB available)")
            logger.info(f"   Disk: {disk.percent}% used ({disk.free // 1024 // 1024 // 1024} GB free)")
            logger.info(f"   CPU Count: {psutil.cpu_count()}")
            logger.info(f"   Start Time: {self.start_time}")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not log system info: {e}")
    
    async def start(self):
        """Start the bot"""
        try:
            await self.initialize()
            
            logger.info("🚀 Starting bot...")
            self.is_running = True
            
            # Setup signal handlers for graceful shutdown
            self.setup_signal_handlers()
            
            # Start the bot
            await self.bot.run()
            
        except KeyboardInterrupt:
            logger.info("⌨️ Received keyboard interrupt")
            await self.shutdown()
        except Exception as e:
            logger.error(f"❌ Fatal error during bot startup: {e}")
            await self.shutdown()
            sys.exit(1)
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"📶 Received signal {signum}")
            asyncio.create_task(self.shutdown())
        
        # Handle SIGINT (Ctrl+C) and SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        if not self.is_running:
            return

logger.info("🛑 Shutting down bot...")
        self.is_running = False
        
        try:
            # Stop the bot application
            if self.bot.application and self.bot.application.running:
                logger.info("🔄 Stopping bot application...")
                await self.bot.application.stop()
                await self.bot.application.shutdown()
                logger.info("✅ Bot application stopped")
            
            # Close database connections
            logger.info("🗄️ Closing database connections...")
            await close_db()
            logger.info("✅ Database connections closed")
            
            # Calculate uptime
            uptime = datetime.now() - self.start_time
            logger.info(f"⏱️ Bot uptime: {uptime}")
            
            logger.info("✅ Bot shutdown completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
        finally:
            # Force exit if needed
            os._exit(0)
    
    async def restart(self):
        """Restart the bot"""
        logger.info("🔄 Restarting bot...")
        await self.shutdown()
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Restart
        os.execv(sys.executable, ['python'] + sys.argv)

async def check_requirements():
    """Check if all requirements are met"""
    logger.info("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8+ is required")
        return False
    
    # Check required environment variables
    required_vars = ['BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("💡 Please check your .env file")
        return False
    
    # Check if bot token is valid format
    token = os.getenv('BOT_TOKEN')
    if not token or ':' not in token or len(token.split(':')) != 2:
        logger.error("❌ Invalid bot token format")
        return False
    
    logger.info("✅ All requirements met")
    return True

async def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'data',
        'backups',
        'temp',
        'uploads'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"📁 Directory ensured: {directory}")

def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 Advanced Telegram Bot Manager v2.0.0              ║
║                                                              ║
║        Features:                                             ║
║        • 25+ Modules with 200+ Commands                     ║
║        • Advanced Anti-Spam Protection                      ║
║        • Comprehensive Moderation Tools                     ║
║        • Multi-Language Support                             ║
║        • Federation System                                  ║
║        • Detailed Logging & Analytics                      ║
║                                                              ║
║        Developer: @YourUsername                              ║
║        Support: @YourSupportGroup                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

async def main():
    """Main entry point"""
    # Print banner
    print_banner()

try:
        # Check requirements first
        if not await check_requirements():
            logger.error("❌ Requirements check failed")
            sys.exit(1)
        
        # Create necessary directories
        await create_directories()
        
        # Initialize and start bot manager
        manager = BotManager()
        await manager.start()
        
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("🏁 Application terminated")

def run_bot():
    """Run the bot with proper event loop handling"""
    try:
        # For Windows compatibility
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Run the main function
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.info("👋 Application interrupted by user")
    except Exception as e:
        logger.error(f"💥 Application crashed: {e}", exc_info=True)
        sys.exit(1)

if name == "main":
    # Set up proper exception handling
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: logger.error(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )
    
    # Run the bot
    run_bot()
`
