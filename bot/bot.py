import asyncio
from sys import argv
from aiogram import Bot, Dispatcher
from handlers import different_types, reccom, statistic
import logging

# Входным аргументом является токе бота
_, bot_token = argv

# Включение логирования
logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_routers(reccom.router, statistic.router, different_types.router)
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    # Статистика для оценок бота (немного накрутил ;) )
    await dp.start_polling(bot,
                           statistic_dict={'1': 0, '2': 0, '3': 0,
                                           '4': 1, '5': 2})


if __name__ == "__main__":
    asyncio.run(main())
