from glob import glob
import os
from random import choice

from db import db, get_or_create_user, subscribe_user, unsubscribe_user, save_burger_image_vote, user_voted, get_image_rating
from jobs import alarm
from utils import play_random_numbers, main_keyboard, is_burger, burger_rating_inline_keyboard, photo_rename


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print('Вызван /start')
    update.message.reply_text(
        f"Привет, {user['first_name']}, ты нажал start {user['emoji']}",
        reply_markup=main_keyboard(),
    )


def send_burger_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    burger_list = glob('images/*burger*.jp*g')
    burger_pic = choice(burger_list)
    chat_id = update.effective_chat.id
    if user_voted(db, burger_pic, user["user_id"]):
        rating = get_image_rating(db, burger_pic)
        keyboard = None
        caption = f"Рейтинг картинки {rating}"
    else:
        keyboard = burger_rating_inline_keyboard(burger_pic)
        caption = None
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(burger_pic, 'rb'),
        reply_markup=keyboard,
        caption=caption
    )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(
        f"Можем повторить {user['emoji']}: " + text,
        reply_markup=main_keyboard()
    )


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
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
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text("Обрабатываем фото")
    os.makedirs('downloads', exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{user_photo.file_id}.jpg')
    user_photo.download(file_name)
    if is_burger(file_name):
        update.message.reply_text('Обнаружен бургер, добавлю его к себе)\nСпасибо!')
        new_name = photo_rename(10)
        new_filename = os.path.join('images', f'burger_{new_name}.jpg')
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text('Бургера нет((\nЯ для тебя какая-то шутка?')
        os.remove(file_name)


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text("Вы успешно подписались!")


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text("Произошла отписка!")


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f"Уведомление через {alarm_seconds} секунд")
    except (ValueError, TypeError):
        update.message.reply_text("Введите целое число секунд после команды")


def burger_picture_rating(update, context):
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split("|")
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    save_burger_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    update.callback_query.edit_message_caption(caption=f"Рейтинг картинки {rating}")
