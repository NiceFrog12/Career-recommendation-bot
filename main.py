import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time
from config import TELEBOT_TOKEN, DATABASE
from logic import *

bot = telebot.TeleBot(TELEBOT_TOKEN)

supported_skills = ["People skills", "Coding", "Cooking", "Multi-lingualism"]


@bot.message_handler(commands=['start'])
def greeting(message):
    # Make the bot look like it's typing for time.sleep() seconds
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    # Sending a welcome message to the person starting the bot
    bot.send_message(message.chat.id, """Hi there! I'm a Telegram bot that's supposed to help you find what you're good at.\n
To start, you can use /register command so that I can remember who you are.""")

@bot.message_handler(commands=['register'])
def add_user_into_database(message):
    # Make an if user in database > "you already registered"
    user_using_id = message.from_user.username
    userlist = list(manager.get_users())
    if user_using_id in userlist:
        bot.send_message(message.chat.id, "You are already registered! Try out other commands, or use /help if you don't know any.")
        return
    try:
        manager.insert_user(user_using_id)
        bot.send_message(message.chat.id, "Succesfully added you into the database!")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Something went wrong. Please try again, and if the problem persists, contact support.")
    
@bot.message_handler(commands=['add'])
def adding_user_skills(message):
    bot.send_message("Here are all the currently supported skills. Select which ones you possess!")
    # MAKE THIS A CALLBACK QUERY WITH AN InlineKeyboard AND ADD THE SKILL TO THE USER



if __name__ == "__main__":
    manager = Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()

    bot.delete_webhook()
    bot.infinity_polling()