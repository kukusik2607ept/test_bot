import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
from handlers import greet_user, guess_number, send_burger_picture, user_coordinates, talk_to_me

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def main():
    # Создание бота и передача ключа
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    # Диспетчер отработки сообщений от пользователя
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("burger", send_burger_picture))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(MessageHandler(Filters.regex("^(Прислать бургер)$"), send_burger_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Сообщение в файл bot.log
    logging.info(u"Start Bot")

    # Командуем боту начать ходить в ТГ за сообщениями
    mybot.start_polling()
    # Запуск бота - работает пока не остановим принудительно
    mybot.idle()


if __name__ == "__main__":
    main()
