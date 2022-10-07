import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!\nI am AboutTheCountryBot. "
                                      f"I can send info about any country!")

print("Bot is working!")

bot.polling(none_stop=True)