from glob import glob
from random import choice

from utils import get_emoji, play_random_numbers, main_keyboard


def greet_user(update, context):
    print('Вызван /start')
    context.user_data['emoji'] = get_emoji(context.user_data)
    update.message.reply_text(
        f"Привет, username, ты нажал start {context.user_data['emoji']}",
        reply_markup=main_keyboard(),
    )


def send_burger_picture(update, context):
    burger_list = glob('images/*burger*.jp*g')
    burger_pic = choice(burger_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(burger_pic, 'rb'),
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    text = update.message.text
    context.user_data['emoji'] = get_emoji(context.user_data)
    print(text)
    update.message.reply_text(
        f"Можем повторить {context.user_data['emoji']}: " + text,
        reply_markup=main_keyboard()
    )


def guess_number(update, context):
    if context.args:
        try:
            number = int(context.args[0])
            message = play_random_numbers(number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(
        message,
        reply_markup=main_keyboard()
    )


def user_coordinates(update, context):
    context.user_data['emoji'] = get_emoji(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}",
        reply_markup=main_keyboard()
    )
