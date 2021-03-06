import telebot, json
import random
import sched
import time
import pandas as pd
from recommender import RecommenderData
from parser import  WikiArtHandler
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
token ='650690422:AAEsDalv8DDRAqZYW-bz_3LhcCrc9NqYujI'
bot = telebot.TeleBot(token)
Counter = {}
s = sched.scheduler(time.time, time.sleep)
recommenders = {}
df = pd.read_csv('df.csv')
df.index = range(3250)
def gen_markup(num):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes " + str(num)), InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
   recommenders[message.chat.id] = RecommenderData()
   bot.send_message(message.chat.id, '''Hello, I am vandal_bot!
If you want to stop working with me send "stop"''')
   #s.enter(0, 1, sendphoto,argument = (message.chat.id))
   r = recommenders[message.chat.id].get_next()
   print(WikiArtHandler.get_pic(df['artist'][r], df['title'][r]))
   bot.send_photo(message.chat.id, WikiArtHandler.get_pic(df['artist'][r], df['title'][r]))
   bot.send_message(message.chat.id,'Answer to me, do you like this picture. Answer only "/yes" or "/no"', reply_markup=gen_markup())
   
def send_photo(message):
   print(1)
   r = recommenders[message.chat.id].get_next()
   bot.send_photo(message, WikiArtHandler.get_pic(df['artist'][r], df['title'][r]))
   if (Counter[message] >= 1):
      print(2)
      s.enter(2, 1, send_photo, argument = (message,))
      s.run()
      

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
   if call.data[:6] == "cb_yes":
      recommenders[call.message.chat.id].update(call.data[7:])
      if (call.message.chat.id in Counter.keys()):
         Counter[call.message.chat.id] = Counter[call.message.chat.id] + 1
      else:
         Counter[call.message.chat.id] = 10
      if Counter[call.message.chat.id] == 10:
         bot.answer_callback_query(call.id, 'If you want to see the pictures of great artistse in any time send me "/anytime"', show_alert=True)
      elif (Counter[call.message.chat.id] > 10):
         s.run()
      else:
         send_photo(call.message.chat.id)
   elif call.data == "cb_no":
      pass

@bot.message_handler(commands=['anytime'])
def aytime(message):
   bot.send_message(message.chat.id,'''If you want to see pictures every hour send me "/hour",
If you want to see pictures every half of day send me "/half_day"
If you want to see pictures every day send me "/day"''')
   
@bot.message_handler(commands=['stop'])
def stop (message):
   bot.send_message(message.chat.id, 'You are the worsest human, that I know! Goodbye!')
   del Counter[message.chat.id]

@bot.message_handler(commands=['hour'])
def every_hour_interval(message):
   s.enter(2, 1, send_photo,argument = (message.chat.id,))
   s.run()
@bot.message_handler(commands=['half_day'])
def every_half_of_day_interval(message):
   s.enter(43200, 1, send_photo,argument = (message.chat.id,))
   s.run()
@bot.message_handler(commands=['day'])
def every_day_interval(message):
   s.enter(86400, 1, send_photo,argument = (message.chat.id,))
   s.run()  
bot.polling(none_stop = True)
