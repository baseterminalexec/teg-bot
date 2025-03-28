from bot.bot import bot, dp

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling())
