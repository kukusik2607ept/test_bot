import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text("Привет, username, ты нажал start")


def talk_to_me(update, context):
    text = update.message.text
    print(text)


def main():
    # Создание бота и передача ключа
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    # Диспетчер отработки сообщений от пользователя
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Сообщение в файл bot.log
    logging.info("Бот стартовал")

    # Командуем боту начать ходить в ТГ за сообщениями
    mybot.start_polling()
    # Запуск бота - работает пока не остановим принудительно
    mybot.idle()


if __name__ == "__main__":
    main()
