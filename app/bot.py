from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
import json

from keyboards import create_keyboard

with open(f'app/config.json', 'rt', encoding='utf-8') as f:
    conf = json.load(f)
bot = Bot(token=conf['TOKEN'], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

button_places = KeyboardButton('Места рядом')
button_route = KeyboardButton('Маршрут')
button_circle_route = KeyboardButton('Кольцевой маршрут')
theme_route = KeyboardButton('Тематический маршрут')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_places)
greet_kb.add(button_route)
greet_kb.add(button_circle_route)
greet_kb.add(theme_route)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    """this is testing method"""
    await message.answer(f"Здравствуйте! Я помогу вам найти интересные места Санкт-Петербурга и области! \n\n"
                         f"Для того, чтобы получить адреса и геопозиции "
                         f"ближайших мест, связанных нажмите на кнопку 'Места рядом' \n\n"
                         f"Чтобы составить маршрут из нескольких мест нажмите на кнопку 'Маршрут' \n\n"
                         f"Чтобы составить кольцевой маршрут в котором  вы начнете с вашей геопозиции "
                         f"и вернетесь туда, где сейчас находитесь нажмите на кнопку 'Кольцевой маршрут'",
                         reply_markup=greet_kb)


@dp.message_handler(content_types=['location'])
async def geolocation_handler(message: types.Message, state: FSMContext):
    """this method handles geolocation from user"""
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(lat=lat, lon=lon)
    await message.answer(f'Введите число мест, которое хотите получить цифрой, например 1',
                         reply_markup=greet_kb)


@dp.message_handler(content_types=['text'])
async def location(message: types.Message, state: FSMContext):
     try:
        n = int(message.text)
        if n <= 0:
            await message.answer("Пожалуйста, введите число больше 0", reply_markup=greet_kb)
        elif n>20:
            await message.answer("Пожалуйста, введите число меньше 20", reply_markup=greet_kb)
        else:
            data = await state.get_data()
            lat = data.get("lat", "Unknown")
            lon = data.get("lon", "Unknown")
            if int(data.get("action", "Unknown")) == 4:
                # places = requests.get(f'{conf["APP"]}/api/closest-places/?coordinate_x=60.000442&coordinate_y=30.329375&amount=2').json()
                places = requests.get(f'{conf["APP"]}/api/closest-places/?coordinate_x={lat}&coordinate_y={lon}&amount={n}').json()
                for place in places:
                    await message.answer_location(latitude=place['coordinate_x'],
                                                  longitude=place['coordinate_y'])
                    await message.answer(f"{place['title']} \n\n {place['description']}",
                                         reply_markup=greet_kb)
            elif data.get("action", "Unknown") == 2:
                places = requests.get(f'{conf["APP"]}/api/closest-route/?coordinate_x={lat}&coordinate_y={lon}&amount={n}').json()
                for place in places:
                    await message.answer_location(latitude=place['coordinate_x'],
                                                  longitude=place['coordinate_y'])
                    await message.answer(f"{place['title']} \n\n {place['description']}",
                                         reply_markup=greet_kb)
            elif data.get("action", "Unknown") == 3:
                places = requests.get(f'{conf["APP"]}/api/circle-route/?coordinate_x={lat}&coordinate_y={lon}&amount={n}').json()
                for place in places[1:]:
                    await message.answer_location(latitude=place['coordinate_x'],
                                                  longitude=place['coordinate_y'])
                    await message.answer(f"{place['title']} \n\n {place['description']}",
                                         reply_markup=greet_kb)
     except Exception:
         if message.text == 'Места рядом':
             await message.answer(
                 f"Отправьте свою геопозицию, чтобы получить список ближайших мест, связанных с литературой",
                 reply_markup=ReplyKeyboardRemove())
             await state.update_data(action=4)
         elif message.text == 'Маршрут':
             await message.answer(
                 f"Отправьте свою геопозицию, чтобы составить маршрут из нескольких мест",
                 reply_markup=ReplyKeyboardRemove())
             await state.update_data(action=2)
         elif message.text == 'Кольцевой маршрут':
             await message.answer(f"Отправьте свою геопозицию, чтобы составить кольцевой маршрут",
                                  reply_markup=ReplyKeyboardRemove())
             await state.update_data(action=3)
         elif message.text == 'Тематический маршрут':
             routes = requests.get(f'{conf["APP"]}/api/route/').json()
             await message.answer(f"Выберите маршрут",
                                  reply_markup=
                                  create_keyboard(list(map(lambda place: f'Маршрут №{place["id"]} : "{place["title"]}"', routes))))
         elif message.text.startswith('Маршрут №'):
             id = str(message.text).split('Маршрут №')[1].split(':')[0]
             routes = requests.get(f'{conf["APP"]}/api/route/{id}/').json()
             await message.answer(f'Маршрут "{routes["title"]}" \nВремя маршрута : {routes["time"]}', reply_markup=greet_kb)
             for place in routes['places']:
                    await message.answer_location(latitude=float(place['coordinate_x']),
                                                  longitude=float(place['coordinate_y']))
                    await message.answer(f"{place['title']} \n\n {place['description']}",
                                         reply_markup=greet_kb)
         else:
             await message.answer(f"Извините, я вас не понимаю", reply_markup=greet_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
