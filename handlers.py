from glob import glob
import os
from random import choice

from utils import get_emoji, play_random_numbers, main_keyboard, is_burger


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


def check_user_photo(update, context):
    update.message.reply_text("Обрабатываем фото")
    os.makedirs('downloads', exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{user_photo.file_id}.jpg')
    user_photo.download(file_name)
    if is_burger(file_name):
        update.message.reply_text('Обнаружен бургер, добавлю его к себе)\nСпасибо!')
        new_filename = os.path.join('images', f'burger_{user_photo.file_id}.jpg')
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text('Бургера нет((\nЯ для тебя какая-то шутка?')
        os.remove(file_name)
