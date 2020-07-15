from emoji import emojize
from glob import glob
import logging
from random import choice, randint

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def get_emoji(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def greet_user(update, context):
    print('Вызван /start')
    context.user_data['emoji'] = get_emoji(context.user_data)
    update.message.reply_text(f"Привет, username, ты нажал start {context.user_data['emoji']}")


def send_burger_picture(update, context):
    burger_list = glob('images/*burger*.jp*g')
    burger_pic = choice(burger_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(burger_pic, 'rb'))


def talk_to_me(update, context):
    text = update.message.text
    context.user_data['emoji'] = get_emoji(context.user_data)
    print(text)
    update.message.reply_text(f"Можем повторить {context.user_data['emoji']}: " + text)


def guess_number(update, context):
    if context.args:
        try:
            number = int(context.args[0])
            message = play_random_numbers(number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, мое {bot_number}, вы проиграли("
    return message


def main():
    # Создание бота и передача ключа
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    # Диспетчер отработки сообщений от пользователя
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("burger", send_burger_picture))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Сообщение в файл bot.log
    logging.info(u"Start Bot")

    # Командуем боту начать ходить в ТГ за сообщениями
    mybot.start_polling()
    # Запуск бота - работает пока не остановим принудительно
    mybot.idle()


if __name__ == "__main__":
    main()
