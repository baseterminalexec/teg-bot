from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.payments import process_payment
from database.database import check_subscription
from config.config import SUBSCRIPTION_AMOUNT

# Inline buttons for commands
def get_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💳 Subscribe", callback_data="subscribe"),
        InlineKeyboardButton("✅ Check Subscription", callback_data="check_status")
    )
    return keyboard

def get_subscription_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📅 1 Month - 10 USDT", callback_data="subscribe_monthly"),
        InlineKeyboardButton("📆 1 Year - 100 USDT", callback_data="subscribe_yearly")
    )
    return keyboard

async def start(message: types.Message):
    await message.answer(
        f"👋 Welcome, {message.from_user.first_name}!\n\n"
        "This bot allows you to subscribe for premium access.\n"
        "💰 Subscription Plans Available:\n"
        "📅 1 Month - 10 USDT\n"
        "📆 1 Year - 100 USDT\n\n"
        "Choose an option below:",
        reply_markup=get_main_menu()
    )

async def button_handler(callback_query: types.CallbackQuery):
    if callback_query.data == "subscribe":
        await callback_query.message.edit_text(
            "Select your subscription plan:",
            reply_markup=get_subscription_menu()
        )
    elif callback_query.data == "subscribe_monthly":
        await callback_query.message.edit_text(
            f"📌 Send 10 USDT to the following wallet:\n\n"
            "💳 Wallet: `your_usdt_trc20_wallet_address`\n\n"
            "After payment, send your transaction ID using:\n"
            "`/confirm <TXID>`"
        )
    elif callback_query.data == "subscribe_yearly":
        await callback_query.message.edit_text(
            f"📌 Send 100 USDT to the following wallet:\n\n"
            "💳 Wallet: `your_usdt_trc20_wallet_address`\n\n"
            "After payment, send your transaction ID using:\n"
            "`/confirm <TXID>`"
        )
    await callback_query.answer()

async def check_subscription_status(callback_query: types.CallbackQuery):
    if check_subscription(callback_query.from_user.id):
        await callback_query.message.edit_text("✅ You have an active subscription! 🎉")
    else:
        await callback_query.message.edit_text("❌ You don't have an active subscription. Use /subscribe to get started.")
    await callback_query.answer()
