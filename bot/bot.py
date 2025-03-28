import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot.handlers import start, confirm_payment, check_subscription_status, button_handler
from bot.payments import approve_subscription
from database.database import init_db
from config.config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()

dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(confirm_payment, commands=['confirm'])
dp.register_message_handler(approve_subscription, commands=['approve'])
dp.register_callback_query_handler(button_handler, lambda c: c.data.startswith('subscribe_'))
dp.register_callback_query_handler(check_subscription_status, lambda c: c.data == 'check_status')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
