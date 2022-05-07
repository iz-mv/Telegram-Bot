from telebot import types
import random
from botfunc import getwiki, send_weather, send_news, con, bot

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM joke")
    rows = cur.fetchall()


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    hello_message = (
        'Привет, {0.first_name}!\nЯ Телеграм-Бот созданный для финального проекта Иcлама и Кирилла в Яндекс.Лицее.'.format(
            message.from_user, bot.get_me()))

    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEpZpidXxE6cNB7vb7qiNC8B0nwmHBwAACAQEAAladvQoivp8OuMLmNCQE")

    item0 = types.KeyboardButton("🌈 Погода")
    item1 = types.KeyboardButton("📰Новости")
    item2 = types.KeyboardButton("🙃Анекдот")
    item4 = types.KeyboardButton("ℹВикипедия")
    markup.add(item0, item1, item2, item4)

    bot.send_message(message.chat.id, hello_message, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_message(message):
    chat_id = message.chat.id
    if message.text == "🌈 Погода":
        msg = bot.send_message(message.chat.id, 'Введите название города/страны:'.format(message.text))
        bot.register_next_step_handler(msg, send_weather)
        print(message.text)

    elif message.text == "📰Новости":
        bot.send_message(message.chat.id, send_news(message))

    elif message.text.strip() == '🙃Анекдот':
        aboba = random.choice(rows)
        bot.send_message(message.chat.id, aboba)

    elif message.text == "ℹВикипедия":
        bot.send_message(message.chat.id, 'Введите интересующее Вас слово/статью:')
        bot.register_next_step_handler(message, getwiki)
        print(message.chat.id, message.text)


bot.polling(none_stop=True, interval=0)
