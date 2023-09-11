import logging
from aiogram import Bot, Dispatcher, executor, types
from service import get_nearest_places, get_simple_route, draw_route, get_circle_route
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Location
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import folium

bot = Bot(token="6481647679:AAH7ApLFgeuBYPkuNM4UnnUYniSLORhkC68", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

button_places = KeyboardButton('Места рядом')
button_route = KeyboardButton('Маршрут')
button_circle_route = KeyboardButton('Кольцевой маршрут')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_places)
greet_kb.add(button_route)
greet_kb.add(button_circle_route)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    """this is testing method"""
    await message.answer(f"Здравствуйте! Я помогу вам найти места, связанные с "
                         f"писателями, поэтами и их произведениями в Санкт-Петербурге! \n\n"
                         f"Для того, чтобы получить адреса и геопозиции "
                         f"ближайших мест, связанных с литературой нажмите на кнопку 'Места рядом' \n\n"
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
            await message.answer(f"Анекдот для шутников:\n"
                                 f"Два часа ночи, бар, все закрыто. Из норки высовывается немецкая мышь, оглядывается — кота нет, несется к бару, наливает себе пива, выпивает и летит что есть сил обратно к норке\n"
                                 f"Через минуту показывается французская мышь, оглядывается — нет кота, тоже несется к бару, наливает себе вина, выпивает и тоже убегает в нору.\n"
                                 f"Выглядывает русская мышь — нет кота, бежит к бару, наливает 100 грамм водяры, выпивает, оглядывается — нет кота, наливает вторую, пьет — нет кота, наливает третью, потом четвертую и пятую… после пятой садится, оглядывается — ну нет кота! — разминает мускулы и злобно так бормочет: 'Ну мы бл@ть подождем…'",

                                 reply_markup=greet_kb)
        elif n>20:
            await message.answer(f"Анекдот для шутников:\n"
                                 f"Два часа ночи, бар, все закрыто. Из норки высовывается немецкая мышь, оглядывается — кота нет, несется к бару, наливает себе пива, выпивает и летит что есть сил обратно к норке\n"
                                 f"Через минуту показывается французская мышь, оглядывается — нет кота, тоже несется к бару, наливает себе вина, выпивает и тоже убегает в нору.\n"
                                 f"Выглядывает русская мышь — нет кота, бежит к бару, наливает 100 грамм водяры, выпивает, оглядывается — нет кота, наливает вторую, пьет — нет кота, наливает третью, потом четвертую и пятую… после пятой садится, оглядывается — ну нет кота! — разминает мускулы и злобно так бормочет: 'Ну мы бл@ть подождем…'",

                                 reply_markup=greet_kb)
        else:
            data = await state.get_data()
            lat = data.get("lat", "Unknown")
            lon = data.get("lon", "Unknown")
            if data.get("action", "Unknown") == 4:
                places = get_nearest_places(my_lon=lat, my_lat=lon, n=n)
                print(places)
                for place in places:
                    await message.answer_location(latitude=place['longitude'],
                                                  longitude=place['latitude'])
                    await message.answer(f"{place['name']} \n\n {place['description']}",
                                         reply_markup=greet_kb)
            elif data.get("action", "Unknown") == 2:
                places = get_simple_route(my_lon=lat, my_lat=lon, n=n)
                print(places)
                for place in places:
                    await message.answer_location(latitude=place['longitude'],
                                                  longitude=place['latitude'])
                    await message.answer(f"{place['name']} \n\n {place['description']}",
                                         reply_markup=greet_kb)
            elif data.get("action", "Unknown") == 3:
                places = get_circle_route(my_lon=lat, my_lat=lon, n=n)
                print(places)
                for place in places[1:]:
                    await message.answer_location(latitude=place['longitude'],
                                                  longitude=place['latitude'])
                    await message.answer(f"{place['name']} \n\n {place['description']}",
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
         else:
             await message.answer(f"Извините, я вас не понимаю", reply_markup=greet_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
