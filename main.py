import os
import logging
from mt5linux import MetaTrader5 # Use the Linux bridge
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from binance.spot import Spot as BinanceClient
from dotenv import load_dotenv

load_dotenv()

# Initialize MT5 with the IP address of your Windows PC/VPS
# Replace 'YOUR_WINDOWS_IP' with the actual IP address
mt5 = MetaTrader5(host='YOUR_WINDOWS_IP', port=8001)

class ProfessionalTradingBot:
    def __init__(self):
        self.is_active = False
        self.binance_client = BinanceClient(api_key=os.getenv("BINANCE_API_KEY"))
        
    async def init_mt5(self):
        """Initializes connection to the MT5 bridge."""
        if not mt5.initialize():
            print(f"MT5 Init Failed: {mt5.last_error()}")
            return False
        return mt5.login(
            int(os.getenv("MT5_LOGIN")), 
            password=os.getenv("MT5_PASSWORD"), 
            server=os.getenv("MT5_SERVER")
        )

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        connected = await self.init_mt5()
        if connected:
            acc = mt5.account_info()
            msg = f"💹 **MT5 Balance**: ${acc.balance}\n"
            msg += f"• Pocket Option UID: {os.getenv('PO_UID')}"
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Could not connect to MT5 Bridge.")

if __name__ == "__main__":
    bot = ProfessionalTradingBot()
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("balance", bot.balance))
    app.run_polling()
