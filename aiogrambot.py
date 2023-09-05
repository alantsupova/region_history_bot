import logging
from aiogram import Bot, Dispatcher, executor, types
from sql import db_start
from service import get_nearest_places
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_hi = KeyboardButton('Места рядом', request_location=True)
# button_places = KeyboardButton('Несколько мест', request_location=True)

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_hi)


bot = Bot(token="6211442274:AAHhyJE609ytFMN-YCn8eGxFyovQB1FNlOg", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    """this is testing method"""
    await message.answer(f"Здравствуйте! Я помогу вам найти места, связанные с "
                         f"писателями, поэтами и их произведениями в Санкт-Петербурге! \n\n"
                         f"Для того, чтобы получить адрес и геопозицию "
                         f"ближайшего места нажмите на кнопку 'Места рядом' \n\n", reply_markup=greet_kb)
                         # f"Чтобы получить адрес и геопозицию нескольких мест - "
                         # f"нажмите на кнопку 'Несколько мест' ", reply_markup=greet_kb)




@dp.message_handler(content_types=['location'])
async def geolocation_handler(message: types.Message):
    """this method handles geolocation from user"""
    lat = message.location.latitude
    lon = message.location.longitude
    places = get_nearest_places(my_lon=lat, my_lat=lon, n=5)
    print(places)
    for place in places:
        await message.answer_location(latitude=place['longitude'], longitude=place['latitude'])
        await message.answer(f"{place['name']} \n\n {place['description']}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)