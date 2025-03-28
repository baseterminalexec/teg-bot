from aiogram import types
from database.database import add_subscription
from config.config import ADMIN_ID

async def process_payment(message: types.Message):
    if len(message.text.split()) < 2:
        await message.reply("❌ Please provide a valid transaction ID: `/confirm TXID`")
        return

    txid = message.text.split()[1]
    await message.bot.send_message(ADMIN_ID, 
                                   f"🛂 **Payment Confirmation Request**\n"
                                   f"👤 User: @{message.from_user.username}\n"
                                   f"🆔 ID: {message.from_user.id}\n"
                                   f"💰 Amount: 10 USDT or 100 USDT\n"
                                   f"🔗 TXID: `{txid}`\n"
                                   "✅ Reply `/approve <user_id>` to confirm.")
    
    await message.reply("✅ Your payment is being reviewed. Please wait for approval.")

async def approve_subscription(message: types.Message):
    if len(message.text.split()) < 2:
        await message.reply("❌ Please provide a valid user ID: `/approve <user_id>`")
        return

    user_id = int(message.text.split()[1])
    user = await message.bot.get_chat(user_id)
    add_subscription(user_id, user.username)
    await message.bot.send_message(user_id, "🎉 Your subscription has been approved! Enjoy premium access!")
    await message.reply(f"✅ Subscription activated for user @{user.username}.")
