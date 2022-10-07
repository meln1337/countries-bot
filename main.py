import telebot
import requests as req
import logging
import sys
import config

bot = telebot.TeleBot(config.TOKEN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def get_population(population):
    if population >= 1e6:
        return f"{population / 1e6}" + " m"
    elif population >= 1e3:
        return f"{population / 1e3}" + " m"
    else:
        return population

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!\n"
                                      f"I am AboutTheCountryBot. I can send info about any country!")
    logger.info("A user typed /start")

@bot.message_handler(commands=['get_info_about_country'])
def get_info_about_country(message):
    country = "".join(message.text.split()[1:])
    res = req.get(f"https://restcountries.com/v2/name/{country}")
    if res.status_code == 404:
        bot.send_message(message.chat.id, "There is no such country!")
        logger.warning(f"A user used get_info_about_country on non-existing country ({country})")
    else:
        data = res.json()[0]
        bot.send_photo(message.chat.id, data['flags']['png'])
        currencies = '\n'.join([ x['name'] + ' (' + x['code'] + ' ' + x['symbol'] + ')' for x in data['currencies']])
        languages = "\n".join([ x['name'] for x in data['languages']] )
        text = f"Full name: {data['name']}\n" \
               f"Capital: {data['capital']}\n" \
               f"Subregion: {data['subregion']}\n" \
               f"Region: {data['region']}\n" \
               f"Population: {get_population(data['population'])}\n" \
               f"Currencies: {currencies}\n" \
               f"Languages: {languages}"
        bot.send_message(message.chat.id, text)
        logger.debug(f"A user used get_info_about_country on {country}")

print("Bot is working!")

bot.polling(none_stop=True)