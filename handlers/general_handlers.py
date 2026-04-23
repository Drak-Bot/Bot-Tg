from telegram import Update
from telegram.ext import CallbackContext

# Start command handler for the OSINT Telegram bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am the OSINT Bot. Here are the available commands:')

# Help command handler for the OSINT Telegram bot
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = "Available commands:\n" 
    help_text += "/start - Start the bot\n"
    help_text += "/help - Show this help message\n"
    help_text += "/osint - Fetch OSINT data\n"
    help_text += "/about - About this bot\n"
    update.message.reply_text(help_text)