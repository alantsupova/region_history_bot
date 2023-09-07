import requests
import time
import json
from service import get_nearest_place

TOKEN = '6211442274:AAHhyJE609ytFMN-YCn8eGxFyovQB1FNlOg'
URL = 'https://api.telegram.org/bot'

def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']

def send_message(chat_id, text):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

def reply_keyboard(chat_id, text):
    reply_markup ={ "keyboard": [["Привет", "Hello"], [{"request_location":True, "text":"Где я нахожусь"}]], "resize_keyboard": True, "one_time_keyboard": True}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def check_message(chat_id, message):
    if message.lower() in ['привет', 'hello']:
        send_message(chat_id, 'Привет :)')
    else:
        reply_keyboard(chat_id, 'Я не понимаю тебя :(')

def run():
    update_id = 0
    if (_update := get_updates()):
        update_id = _update[-1]['update_id']
    while True:
        time.sleep(2)
        messages = get_updates(update_id) # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id']# Сохраняем ID последнего отправленного сообщения боту
                if (user_message := message['message'].get('text')): # Проверим, есть ли текст в сообщении
                    check_message(message['message']['chat']['id'], user_message) # Отвечаем
                if (user_location := message['message'].get('location')): # Проверим, если ли location в сообщении
                    print(user_location)
if __name__ == '__main__':
    run()