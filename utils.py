from random import choice, randint
from string import ascii_letters

from clarifai.rest import ClarifaiApp
from pprint import PrettyPrinter
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import settings


def main_keyboard():
    return ReplyKeyboardMarkup(
        [['Прислать бургер', KeyboardButton('Прислать мои координаты', request_location=True)], ["Заполнить анкету"]])


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, мое {bot_number}, вы проиграли("
    return message


def is_burger(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=20)
    if response['status']['code'] == 10000:
        print(response)
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'burger':
                return True
    return False


def burger_rating_inline_keyboard(image_name):
    callback_text = f"Rating|{image_name}|"
    keyboard = [
        [
            InlineKeyboardButton('Like', callback_data=callback_text + '1'),
            InlineKeyboardButton('Dislike', callback_data=callback_text + '-1')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def photo_rename(length):
    letters = ascii_letters
    burger_name = ''
    for i in range(length):
        burger_name += choice(letters)
    return burger_name
