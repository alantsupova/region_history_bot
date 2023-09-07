import logging
from aiogram import Bot, Dispatcher, executor, types
from service import get_nearest_places, get_simple_route, draw_route
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Location
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import folium

bot = Bot(token="6211442274:AAHhyJE609ytFMN-YCn8eGxFyovQB1FNlOg", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

button_hi = KeyboardButton('Места рядом', request_location=True)
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_hi)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    """this is testing method"""
    await message.answer(f"Здравствуйте! Я помогу вам найти места, связанные с "
                         f"писателями, поэтами и их произведениями в Санкт-Петербурге! \n\n"
                         f"Для того, чтобы получить адрес и геопозицию "
                         f"ближайшего места нажмите на кнопку 'Места рядом' \n\n",
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
            places = get_simple_route(my_lon=lat, my_lat=lon, n=n)
            print(places)
            draw_route(places)
            for place in places:
                await message.answer_location(latitude=place['longitude'],
                                              longitude=place['latitude'])
                await message.answer(f"{place['name']} \n\n {place['description']}",
                                     reply_markup=greet_kb)
            with open('map.html', 'rb') as f:
                await bot.send_document(chat_id=message.chat.id, document=f)
    # except Exception:
    #     print(Exception)
    #     await message.answer(f"Извините, я вас не понимаю", reply_markup=greet_kb)


# @dp.callback_query_handlers()
# async def callback(call):
#     if call == 'change_geo':
#         call.message.answer('df',  request_location=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
