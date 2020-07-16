from random import choice, randint

from clarifai.rest import ClarifaiApp
from emoji import emojize
from pprint import PrettyPrinter
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


def get_emoji(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать бургер', KeyboardButton('Прислать мои координаты', request_location=True)]])


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

