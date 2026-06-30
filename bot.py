import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN", "")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("Please add BOT_TOKEN in Railway Variables tab")
    exit(1)

print(f"✅ Token loaded successfully (length: {len(TOKEN)})")

# ===== Helper Functions =====
def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def count_characters(text: str) -> int:
    """Count total characters including spaces"""
    return len(text)

def count_characters_no_spaces(text: str) -> int:
    """Count characters excluding spaces"""
    return len(text.replace(" ", ""))

def count_sentences(text: str) -> int:
    """Count sentences using ., !, ? as delimiters"""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def count_paragraphs(text: str) -> int:
    """Count paragraphs by splitting on double newlines"""
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])

def count_lines(text: str) -> int:
    """Count lines in text"""
    lines = text.split('\n')
    return len([l for l in lines if l.strip()])

def estimate_reading_time(word_count: int) -> str:
    """Estimate reading time (200 words per minute avg)"""
    if word_count == 0:
        return "0 seconds"
    minutes = word_count / 200
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    else:
        return f"{minutes:.1f} minute{'s' if minutes != 1 else ''}"

def count_letters(text: str) -> dict:
    """Count frequency of each letter (a-z)"""
    letter_count = {}
    for char in text.lower():
        if char.isalpha():
            letter_count[char] = letter_count.get(char, 0) + 1
    # Sort by count descending
    return dict(sorted(letter_count.items(), key=lambda x: x[1], reverse=True))

def count_numbers(text: str) -> int:
    """Count numbers in text"""
    return len(re.findall(r'\d+', text))

# ===== Command Handlers =====
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_msg = (
        f"✍️ *Hello {user.first_name}!*\n\n"
        "Welcome to *WordstartxBot* - your word counting companion!\n\n"
        "📊 *What I can do:*\n"
        "• Count words, characters, sentences\n"
        "• Count paragraphs, lines, and numbers\n"
        "• Show letter frequency\n"
        "• Estimate reading time\n\n"
        "🔹 *How to use:*\n"
        "Just send me any text, and I'll analyze it!\n"
        "Send /help to see all commands."
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_msg = (
        "📖 *WordstartxBot Help*\n\n"
        "*Commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/stats - Show bot statistics\n"
        "/about - About this bot\n\n"
        "*Text Analysis:*\n"
        "Simply send any text message and I'll provide:\n"
        "• Word count\n"
        "• Character count (with and without spaces)\n"
        "• Sentence count\n"
        "• Paragraph count\n"
        "• Line count\n"
        "• Number count\n"
        "• Letter frequency (most common letters)\n"
        "• Estimated reading time\n\n"
        "*Tips:*\n"
        "• Send long texts for detailed analysis\n"
        "• Works with any language\n"
        "• All processing is done in real-time"
    )
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    stats_msg = (
        "📊 *Bot Statistics*\n\n"
        "This bot is powered by:\n"
        "• Python 3.x\n"
        "• python-telegram-bot library\n"
        "• Deployed on Railway\n\n"
        "⚡ *Features:*\n"
        "• Real-time text analysis\n"
        "• Accurate counting algorithms\n"
        "• Fast response time\n"
        "• Privacy-focused (we don't store your text)"
    )
    await update.message.reply_text(stats_msg, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_msg = (
        "📝 *About WordstartxBot*\n\n"
        "This bot was created to help writers, students, and professionals "
        "quickly analyze text for word and character counts.\n\n"
        "*Why WordstartxBot?*\n"
        "✓ Simple and fast\n"
        "✓ No registration needed\n"
        "✓ Privacy-focused (we don't store your text)\n"
        "✓ Free to use\n"
        "✓ Detailed letter frequency analysis\n\n"
        "Built with ❤️ using open-source tools."
    )
    await update.message.reply_text(about_msg, parse_mode='Markdown')

# ===== Message Handler =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages"""
    text = update.message.text
    
    if text.startswith('/'):
        return
    
    if len(text.strip()) == 0:
        await update.message.reply_text("⚠️ Please send some text to analyze!")
        return
    
    # Perform calculations
    word_count = count_words(text)
    char_count = count_characters(text)
    char_no_space = count_characters_no_spaces(text)
    sentence_count = count_sentences(text)
    paragraph_count = count_paragraphs(text)
    line_count = count_lines(text)
    number_count = count_numbers(text)
    reading_time = estimate_reading_time(word_count)
    
    # Get letter frequency (top 5)
    letter_freq = count_letters(text)
    top_letters = ""
    if letter_freq:
        top_items = list(letter_freq.items())[:5]
        top_letters = "\n".join([f"• `{letter}`: {count} times" for letter, count in top_items])
        if len(letter_freq) > 5:
            top_letters += f"\n• *...and {len(letter_freq) - 5} more letters*"
    else:
        top_letters = "No letters found"
    
    # Format the response
    response = (
        f"📊 *Text Analysis Results*\n"
        f"{'─' * 30}\n"
        f"📝 *Words:* {word_count:,}\n"
        f"🔤 *Characters:* {char_count:,}\n"
        f"⬜ *Characters (no spaces):* {char_no_space:,}\n"
        f"📄 *Sentences:* {sentence_count:,}\n"
        f"📑 *Paragraphs:* {paragraph_count:,}\n"
        f"📏 *Lines:* {line_count:,}\n"
        f"🔢 *Numbers:* {number_count:,}\n"
        f"⏱️ *Reading time:* {reading_time}\n"
        f"{'─' * 30}\n"
        f"📊 *Top 5 Letters:*\n{top_letters}\n"
        f"{'─' * 30}\n"
        f"📎 *Text preview:*\n"
        f"`{text[:100]}{'...' if len(text) > 100 else ''}`"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

# ===== Error Handler =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    print(f"❌ Error: {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ An error occurred. Please try again.")

# ===== Main Function =====
def main():
    """Start the bot"""
    print("🚀 Starting WordstartxBot...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Application built successfully")
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(CommandHandler("about", about_command))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot is running! Waiting for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
