import os
import asyncio
import json
import websockets
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from binance.spot import Spot as BinanceClient
from dotenv import load_dotenv

load_dotenv()

class PocketOptionBot:
    def __init__(self):
        self.is_active = False
        self.binance_client = BinanceClient(api_key=os.getenv("BINANCE_API_KEY"))
        self.po_uid = os.getenv("PO_UID")
        self.session_token = os.getenv("PO_SESSION_TOKEN")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.is_active = True
        await update.message.reply_text(f"🚀 **Bot Online!**\nMonitoring Pocket Option (UID: {self.po_uid})\nType /status to check connection.")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Basic status check
        msg = (
            "📊 **Bot Status**\n"
            f"• Mode: {'Active' if self.is_active else 'Paused'}\n"
            f"• Pocket Option UID: {self.po_uid}\n"
            "• Market Data: Binance API Connected"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    async def get_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Example fetching Bitcoin price from Binance
        ticker = self.binance_client.ticker_price("BTCUSDT")
        price = float(ticker['price'])
        await update.message.reply_text(f"💰 **Current BTC Price**: ${price:,.2f}")

if __name__ == "__main__":
    bot = PocketOptionBot()
    
    # Build the Telegram Application
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    
    # Add Handlers
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("status", bot.status))
    app.add_handler(CommandHandler("price", bot.get_price))
    
    print("Railway: Bot is starting up...")
    app.run_polling()
