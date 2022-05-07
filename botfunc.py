import telebot
import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3
import wikipedia
import pyowm

con = sqlite3.connect("jokedb.db")

wikipedia.set_lang("ru")

owm = pyowm.OWM('4ca0ed50f846cf4d08ac7097a89b9ff3', language='ru')

bot = telebot.TeleBot('5146513386:AAHXpSJfhjTj5dIYeef_yW-pdAr02LJaKv8')


def getwiki(s):
    try:
        ny = wikipedia.page(s.text)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        bot.send_message(s.chat.id, wikitext2)

    except Exception as e:
        bot.send_message(s.chat.id, text='Кажется, даже Википедия не знает что это)')


def send_weather(message):  # функция отправки погоды
    try:
        observation = owm.weather_at_place(message.text)
        print(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']

        answer = 'В ' + message.text + ' сейчас ' + w.get_detailed_status() + '\n'
        answer += 'Температура в районе ' + str(temp) + '°C ' + '\n\n'
        # шаблоны текстов

        if temp < 0:  # температура ниже 0 гр
            answer += 'Погода совсем не весенняя, лучше одеться потеплее'
        elif temp < 10:  # 0 - 10 гр
            answer += 'Погода довольно приятная, но лучше взять с собой пальто'
        elif temp < 20:  # 10 - 20 гр
            answer += 'Отличная погода для прогулки в лёгкой одежде'
        elif temp < 30:  # 20 - 30 гр
            answer += 'Советую выходить на улицу в шортах и футболке)'
        else:
            answer += ''

        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, 'Кажется, я не знаю такой город/страну')


def send_news(message):
    try:
        URL_TEMPLATE = 'https://yandex.ru/news'
        r = requests.get(URL_TEMPLATE)

        soup = bs(r.text, "html.parser")
        tegg = soup.find_all('div', class_='mg-card__annotation')

        hui = str(tegg)

        s1 = hui.replace('<div class="mg-card__annotation">', "")
        s2 = s1.replace('</div>, ', '\n \n')
        s3 = s2.replace('[', '')
        s4 = s3.replace(']', '')

        print(s4)
        bot.send_message(message.chat.id, s4[:500] + "... \nПродолжение: https://yandex.ru/news")

    except Exception:
        bot.send_message(message.chat.id, "Для перезапуска бота напишите: '/start'")
