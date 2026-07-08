import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USERNAME = os.getenv('PLP_USERNAME')
PASSWORD = os.getenv('PLP_PASSWORD')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def plp_action(action_type: str) -> str:
    """Performs the check-in or check-out action on PLP via Playwright."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            logger.info("Navigating to login page...")
            await page.goto("https://plp.moeys.gov.kh/teacher-attendance", wait_until="networkidle")
            
            # Login
            await page.fill("#userName", USERNAME)
            await page.fill("#password", PASSWORD)
            await page.click(".login-submit-btn")
            
            logger.info("Waiting for login to complete...")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Navigate back to attendance page
            logger.info("Navigating to attendance page...")
            await page.goto("https://plp.moeys.gov.kh/teacher-attendance", wait_until="networkidle")
            await asyncio.sleep(2)
            
            # Click the target button
            if action_type == 'checkin':
                button = page.get_by_role("button", name="កត់ត្រាចូល")
            else:
                button = page.get_by_role("button", name="កត់ត្រាចេញ")
            
            if await button.count() > 0:
                await button.click()
                await asyncio.sleep(2)
                await browser.close()
                return "✅ ជោគជ័យ! ប្រតិបត្តិការរបស់អ្នកត្រូវបានកត់ត្រា។"
            else:
                await browser.close()
                return "❌ បរាជ័យ! រកមិនឃើញប៊ូតុងសម្រាប់ចុចនៅលើប្រព័ន្ធទេ។ វាអាចដោយសារតែអ្នកបានចុចរួចហើយ ឬប្រព័ន្ធមានបញ្ហា។"

    except Exception as e:
        logger.error(f"Error during {action_type}: {e}")
        return f"❌ មានបញ្ហាបច្ចេកទេស៖ {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    reply_keyboard = [['/checkin', '/checkout']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(
        "សួស្ដី! ខ្ញុំគឺជា Bot សម្រាប់ Check-in និង Check-out នៅលើប្រព័ន្ធ PLP។\n\n"
        "សូមជ្រើសរើសពាក្យបញ្ជាខាងក្រោម៖",
        reply_markup=markup
    )

async def check_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /checkin command."""
    await update.message.reply_text("⏳ កំពុងដំណើរការ Check-in ចូលប្រព័ន្ធ... សូមរង់ចាំបន្តិច។")
    result = await plp_action('checkin')
    await update.message.reply_text(result)

async def check_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /checkout command."""
    await update.message.reply_text("⏳ កំពុងដំណើរការ Check-out ចេញពីប្រព័ន្ធ... សូមរង់ចាំបន្តិច។")
    result = await plp_action('checkout')
    await update.message.reply_text(result)

if __name__ == '__main__':
    if not TOKEN or TOKEN == 'your_token_here':
        logger.error("Please set TELEGRAM_BOT_TOKEN in your .env file.")
        exit(1)
    if not USERNAME or not PASSWORD:
        logger.error("Please set PLP_USERNAME and PLP_PASSWORD in your .env file.")
        exit(1)
        
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("checkin", check_in))
    app.add_handler(CommandHandler("checkout", check_out))

    logger.info("Bot is running...")
    app.run_polling()
