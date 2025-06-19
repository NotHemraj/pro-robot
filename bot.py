import asyncio
import logging
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
from config import Config
from logging_config import setup_logging
from helpers.logger import get_logger
from database.models import init_db
from helpers.decorators import rate_limit
from helpers.functions import extract_user_and_text, get_user_id
import importlib
import sys

# Setup logging
setup_logging()
logger = get_logger(__name__)

class TelegramBot:
    def __init__(self):
        self.application = None
        self.modules = []
        self.commands = []

    async def setup(self):
        """Initialize bot and load modules"""
        try:
            # Create application
            self.application = Application.builder().token(Config.TOKEN).build()

            # Initialize database
            await init_db()
            logger.info("Database initialized successfully")

            # Load all modules
            await self.load_modules()

            # Add basic handlers
            self.add_basic_handlers()

            # Add error handler
            self.application.add_error_handler(self.error_handler)

            # Set bot commands
            await self.set_bot_commands()

        except Exception as e:
            logger.error(f"Failed to setup bot: {e}")
            raise

    async def load_modules(self):
        """Load all command modules"""
        module_names = [
            'modules.admin',
            'modules.antiflood',
            'modules.antiraid',
            'modules.approval',
            'modules.bans',
            'modules.blocklists',
            'modules.captcha',
            'modules.clean_comma',
            'modules.clean_service',
            'modules.connections',
            'modules.disabling',
            'modules.federations',
            'modules.filters',
            'modules.formatting',
            'modules.greetings',
            'modules.import_export',
            'modules.languages',
            'modules.locks',
            'modules.log_channels',
            'modules.misc',
            'modules.notes',
            'modules.pin',
            'modules.privacy',
            'modules.purges',
            'modules.reports',
            'modules.rules',
            'modules.topics'
        ]

        for module_name in module_names:
            try:
                # Import module
                module = importlib.import_module(module_name)

                # Register handlers if module has the function
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(self.application)

                # Collect commands for help
                if hasattr(module, 'COMMANDS'):
                    self.commands.extend(module.COMMANDS)

                self.modules.append(module)
                logger.info(f"✅ Loaded module: {module_name}")

            except ImportError as e:
                logger.error(f"❌ Module {module_name} not found: {e}")
            except Exception as e:
                logger.error(f"❌ Failed to load module {module_name}: {e}")

    def add_basic_handlers(self):
        """Add basic bot handlers"""

        # Start command
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /start command"""
            user = update.effective_user
            chat = update.effective_chat

            if chat.type == 'private':
                text = (
                    f"Hello {user.first_name}! 👋\n\n"
                    f"I'm an advanced Telegram group management bot with many useful features:\n\n"
                    f"🛡️ <b>Anti-spam Protection</b>\n"
                    f"• Anti-flood and anti-raid systems\n"
                    f"• Advanced content filters\n"
                    f"• CAPTCHA verification\n\n"
                    f"👮‍♂️ <b>Moderation Tools</b>\n"
                    f"• Warn, mute, kick, ban users\n"
                    f"• Message purging\n"
                    f"• User reports system\n\n"
                    f"🔧 <b>Administration</b>\n"
                    f"• Channel locks and restrictions\n"
                    f"• Welcome/goodbye messages\n"
                    f"• Notes and rules management\n\n"
                    f"📊 <b>Logging & Analytics</b>\n"
                    f"• Comprehensive action logging\n"
                    f"• Federation system\n"
                    f"• Import/export settings\n\n"
                    f"Use /help to see all available commands!\n\n"
                    f"Add me to your group and make me admin to get started! 🚀"
                )

                keyboard = [
                    [InlineKeyboardButton("📚 Commands", callback_data="help_main")],
                    [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
                    [InlineKeyboardButton("💬 Support", url="https://t.me/YourSupportGroup")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

            else:
                text = (
                    f"Hello! I'm alive and working in this group! ✅\n"
                    f"Use /help to see available commands."
                )
                reply_markup = None

            await update.message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )

        # Help command
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /help command"""
            keyboard = [
                [InlineKeyboardButton("🛡️ Admin", callback_data="help_admin"),
                 InlineKeyboardButton("👮‍♂️ Moderation", callback_data="help_moderation")],
                [InlineKeyboardButton("🔒 Anti-Spam", callback_data="help_antispam"),
                 InlineKeyboardButton("🔐 Security", callback_data="help_security")],
                [InlineKeyboardButton("🔧 Utilities", callback_data="help_utilities"),
                 InlineKeyboardButton("⚙️ Config", callback_data="help_config")],
                [InlineKeyboardButton("📊 Logs", callback_data="help_logs"),
                 InlineKeyboardButton("🌐 Federation", callback_data="help_federation")],
                [InlineKeyboardButton("🎯 Miscellaneous", callback_data="help_misc")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            text = (
                f"🤖 <b>Bot Help Menu</b>\n\n"
                f"Select a category to view available commands:\n\n"
                f"<i>Note: Some commands require admin privileges</i>"
            )

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(
                    text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )

        # About command
        async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /about command"""

            text = (
                f"🤖 <b>Advanced Telegram Bot</b>\n\n"
                f"<b>Version:</b> 2.0.0\n"
                f"<b>Python:</b> {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
                f"<b>Library:</b> python-telegram-bot\n\n"
                f"<b>Features:</b>\n"
                f"• 25+ modules with 200+ commands\n"
                f"• Advanced anti-spam protection\n"
                f"• Comprehensive moderation tools\n"
                f"• Multi-language support\n"
                f"• Federation system\n"
                f"• Detailed logging\n\n"
                f"<b>Developer:</b> @YourUsername\n"
                f"<b>Support:</b> @YourSupportGroup"
            )

            keyboard = [
                [InlineKeyboardButton("📚 Commands", callback_data="help_main")],
                [InlineKeyboardButton("🔗 Source", url="https://github.com/yourusername/telegram-bot")],
                [InlineKeyboardButton("💬 Support", url="https://t.me/YourSupportGroup")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )

        # Stats command
        async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /stats command"""
            from database.functions import get_stats

            stats_data = await get_stats()

            text = (
                f"📊 <b>Bot Statistics</b>\n\n"
                f"👥 <b>Users:</b> {stats_data.get('users', 0):,}\n"
                f"💬 <b>Chats:</b> {stats_data.get('chats', 0):,}\n"
                f"🚨 <b>Bans:</b> {stats_data.get('bans', 0):,}\n"
                f"⚠️ <b>Warns:</b> {stats_data.get('warns', 0):,}\n"
                f"🔍 <b>Filters:</b> {stats_data.get('filters', 0):,}\n"
                f"📝 <b>Notes:</b> {stats_data.get('notes', 0):,}\n"
                f"🌐 <b>Federations:</b> {stats_data.get('federations', 0):,}\n\n"
                f"⏱️ <b>Uptime:</b> {stats_data.get('uptime', 'Unknown')}\n"
                f"💾 <b>Memory Usage:</b> {stats_data.get('memory', 'Unknown')}"
            )

            await update.message.reply_text(text, parse_mode=ParseMode.HTML)

        # Ping command
        async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /ping command"""
            import time
            start_time = time.time()
            message = await update.message.reply_text("🏓 Pinging...")
            end_time = time.time()

            ping_time = round((end_time - start_time) * 1000, 2)

            await message.edit_text(
                f"🏓 <b>Pong!</b>\n"
                f"⚡ Response time: {ping_time}ms",
                parse_mode=ParseMode.HTML
            )

        # Register basic handlers
        self.application.add_handler(CommandHandler('start', start))
        self.application.add_handler(CommandHandler('help', help_command))
        self.application.add_handler(CommandHandler('about', about))
        self.application.add_handler(CommandHandler('stats', stats))
        self.application.add_handler(CommandHandler('ping', ping))

        # Callback query handler for help menu
        self.application.add_handler(CallbackQueryHandler(self.handle_help_callback, pattern=r'^help_'))

    async def handle_help_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle help menu callbacks"""
        query = update.callback_query
        await query.answer()

        category = query.data.replace('help_', '')

        help_texts = {
            'main': self.get_main_help(),
            'admin': self.get_admin_help(),
            'moderation': self.get_moderation_help(),
            'antispam': self.get_antispam_help(),
            'security': self.get_security_help(),
            'utilities': self.get_utilities_help(),
            'config': self.get_config_help(),
            'logs': self.get_logs_help(),
            'federation': self.get_federation_help(),
            'misc': self.get_misc_help()
        }

        text = help_texts.get(category, "Unknown category")

        # Back button
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="help_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

    def get_main_help(self):
        """Get main help text"""
        return (
            f"🤖 <b>Bot Help Menu</b>\n\n"
            f"Select a category to view available commands:\n\n"
            f"🛡️ <b>Admin</b> - Administrative commands\n"
            f"👮‍♂️ <b>Moderation</b> - Moderation tools\n"
            f"🔒 <b>Anti-Spam</b> - Anti-spam protection\n"
            f"🔐 <b>Security</b> - Security features\n"
            f"🔧 <b>Utilities</b> - Utility commands\n"
            f"⚙️ <b>Config</b> - Configuration\n"
            f"📊 <b>Logs</b> - Logging system\n"
            f"🌐 <b>Federation</b> - Federation system\n"
            f"🎯 <b>Miscellaneous</b> - Other commands\n\n"
            f"<i>Commands marked with * require admin privileges</i>"
        )

    def get_admin_help(self):
        """Get admin help text"""
        return (
            f"🛡️ <b>Admin Commands</b>\n\n"
            f"<code>/adminlist</code> - List all admins\n"
            f"<code>/admins</code> - Ping all admins\n"
            f"<code>/promote</code>* - Promote user to admin\n"
            f"<code>/demote</code>* - Demote admin to user\n"
            f"<code>/pin</code>* - Pin a message\n"
            f"<code>/unpin</code>* - Unpin message\n"
            f"<code>/unpinall</code>* - Unpin all messages\n"
            f"<code>/invitelink</code>* - Get invite link\n"
            f"<code>/leave</code>* - Make bot leave chat\n"
            f"<code>/chatinfo</code> - Get chat information\n"
            f"<code>/id</code> - Get user/chat ID\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_moderation_help(self):
        """Get moderation help text"""
        return (
            f"👮‍♂️ <b>Moderation Commands</b>\n\n"
            f"<code>/warn</code>* - Warn a user\n"
            f"<code>/warns</code> - Check user warns\n"
            f"<code>/unwarn</code>* - Remove a warn\n"
            f"<code>/kick</code>* - Kick a user\n"
            f"<code>/ban</code>* - Ban a user\n"
            f"<code>/unban</code>* - Unban a user\n"
            f"<code>/mute</code>* - Mute a user\n"
            f"<code>/unmute</code>* - Unmute a user\n"
            f"<code>/purge</code>* - Delete messages\n"
            f"<code>/del</code>* - Delete replied message\n"
            f"<code>/report</code> - Report a user\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_antispam_help(self):
        """Get anti-spam help text"""
        return (
            f"🔒 <b>Anti-Spam Commands</b>\n\n"
            f"<code>/antiflood</code>* - Configure anti-flood\n"
            f"<code>/antiraid</code>* - Configure anti-raid\n"
            f"<code>/filter</code>* - Add content filter\n"
            f"<code>/filters</code> - List all filters\n"
            f"<code>/stop</code>* - Remove filter\n"
            f"<code>/locks</code>* - View/set locks\n"
            f"<code>/lock</code>* - Lock content type\n"
            f"<code>/unlock</code>* - Unlock content type\n"
            f"<code>/blocklist</code>* - Manage blocklists\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_security_help(self):
        """Get security help text"""
        return (
            f"🔐 <b>Security Commands</b>\n\n"
            f"<code>/captcha</code>* - Configure CAPTCHA\n"
            f"<code>/approval</code>* - Approval mode settings\n"
            f"<code>/approve</code>* - Approve a user\n"
            f"<code>/unapprove</code>* - Unapprove a user\n"
            f"<code>/approved</code> - List approved users\n"
            f"<code>/privacy</code>* - Privacy settings\n"
            f"<code>/blacklist</code>* - User blacklist\n"
            f"<code>/whitelist</code>* - User whitelist\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_utilities_help(self):
        """Get utilities help text"""
        return (
            f"🔧 <b>Utility Commands</b>\n\n"
            f"<code>/save</code>* - Save a note\n"
            f"<code>/get</code> - Get a note\n"
            f"<code>/notes</code> - List all notes\n"
            f"<code>/clear</code>* - Clear a note\n"
            f"<code>/rules</code> - View chat rules\n"
            f"<code>/setrules</code>* - Set chat rules\n"
            f"<code>/topics</code>* - Manage topics\n"
            f"<code>/settopic</code>* - Set topic\n"
            f"<code>/weather</code> - Get weather info\n"
            f"<code>/time</code> - Get time info\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_config_help(self):
        """Get configuration help text"""
        return (
            f"⚙️ <b>Configuration Commands</b>\n\n"
            f"<code>/welcome</code>* - Welcome settings\n"
            f"<code>/goodbye</code>* - Goodbye settings\n"
            f"<code>/setwelcome</code>* - Set welcome message\n"
            f"<code>/setgoodbye</code>* - Set goodbye message\n"
            f"<code>/language</code>* - Set language\n"
            f"<code>/connection</code>* - Connection settings\n"
            f"<code>/disable</code>* - Disable commands\n"
            f"<code>/enable</code>* - Enable commands\n"
            f"<code>/disabled</code> - List disabled commands\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_logs_help(self):
        """Get logs help text"""
        return (
            f"📊 <b>Logging Commands</b>\n\n"
            f"<code>/log</code>* - Set log channel\n"
            f"<code>/nolog</code>* - Disable logging\n"
            f"<code>/logchannel</code> - Current log channel\n"
            f"<code>/formatting</code>* - Log formatting\n"
            f"<code>/export</code>* - Export chat data\n"
            f"<code>/import</code>* - Import chat data\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_federation_help(self):
        """Get federation help text"""
        return (
            f"🌐 <b>Federation Commands</b>\n\n"
            f"<code>/newfed</code> - Create federation\n"
            f"<code>/delfed</code> - Delete federation\n"
            f"<code>/joinfed</code>* - Join federation\n"
            f"<code>/leavefed</code>* - Leave federation\n"
            f"<code>/fedinfo</code> - Federation info\n"
            f"<code>/fban</code> - Federation ban\n"
            f"<code>/funban</code> - Federation unban\n"
            f"<code>/fedadmins</code> - Federation admins\n\n"
            f"<i>* Admin only commands</i>"
        )

    def get_misc_help(self):
        """Get miscellaneous help text"""
        return (
            f"🎯 <b>Miscellaneous Commands</b>\n\n"
            f"<code>/start</code> - Start the bot\n"
            f"<code>/help</code> - Show this help\n"
            f"<code>/about</code> - About the bot\n"
            f"<code>/stats</code> - Bot statistics\n"
            f"<code>/ping</code> - Check bot response\n"
            f"<code>/paste</code> - Paste text content\n"
            f"<code>/regex</code> - Test regex patterns\n"
            f"<code>/reverse</code> - Reverse search image\n"
            f"<code>/ud</code> - Urban dictionary\n"
            f"<code>/wiki</code> - Wikipedia search\n\n"
            f"<i>Fun and utility commands</i>"
        )

    async def set_bot_commands(self):
        """Set bot commands for the command menu"""
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Get help and command list"),
            BotCommand("about", "About the bot"),
            BotCommand("stats", "Bot statistics"),
            BotCommand("ping", "Check bot response time"),
            BotCommand("adminlist", "List all admins"),
            BotCommand("rules", "View chat rules"),
            BotCommand("notes", "List saved notes"),
            BotCommand("filters", "List active filters"),
            BotCommand("warns", "Check your warnings"),
            BotCommand("report", "Report a user/message"),
            BotCommand("id", "Get user/chat ID information")
        ]

        try:
            await self.application.bot.set_my_commands(commands)
            logger.info("Bot commands set successfully")
        except Exception as e:
            logger.error(f"Failed to set bot commands: {e}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")

        # Try to send error message to user
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ An error occurred while processing your request. "
                    "Please try again later or contact support if the issue persists."
                )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

    async def run(self):
        """Start the bot"""
        try:
            await self.setup()
            logger.info("🚀 Bot started successfully!")
            logger.info(f"Bot username: @{(await self.application.bot.get_me()).username}")
            await self.application.run_polling()
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise

# Global bot instance
bot = TelegramBot()

# For backwards compatibility
application = bot.application
