import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города, я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {  # Забираю данные из  сформированного json для того чтобы подставить эмоджи
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'

    }

    try:
        r = requests.get(  # Подсветилась библиотека requests
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )  # Сформировал запрос
        data = r.json()
        # pprint(data)
        # Забираю данные из  сформированного json
        city = data['name']  # Город
        cur_weather = data['main']['temp']  # Температура

        weather_description = data['weather'][0]['main']  # Вид погоды + эмоджи
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Погода в окно, не пойму что там за погода!'

        humidity = data['main']['humidity']  # Влажность
        pressure = data['main']['pressure']  # Давление
        wind = data['wind']['speed']  # Скорость ветра
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        # Заполняю плейсхолдеры
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f'Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n'
              f'Влажность: {humidity}%\nДавление: {pressure}  мм.рт.ст\nВетер: {wind} м/с\n'
              f'Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {length_of_day}\n'
              f'***Хорошего дня***'
              )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)