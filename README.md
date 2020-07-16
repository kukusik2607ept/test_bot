# Проект TestBot

TestBot - это бот для Telegram, который выполняет несколько вещей:
1) он присылает вам бургеры по вашей просьбе.
2) и так далее


## Установка

1. Клонируйте репозиторий в github
2. Создайте и запустите виртуальное окружение
    a.python -m venv env - создание
    b.env\Scripts\activate.bat - запуск    
3. Установите зависимости 'pip install -r requirements.txt'
4. Создайте файл 'settings.py'
5. Впишите в settings.py переменные
'''
API_KEY = "API-ключ бота"
PROXY_URL = "Адрес прокси"
PROXY_USERNAME = "Логин прокси"
PROXY_PASSWORD = "Пароль прокси"
USER_EMOJI = [':hamburger:', ':pizza:', ':fries:',':beer:'] - список использующихся эмодзи

6. Запустите бота командой 'python bot.py'


