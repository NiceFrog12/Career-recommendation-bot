import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import time
import re
from config import TELEBOT_TOKEN, DATABASE
from logic import *

bot = telebot.TeleBot(TELEBOT_TOKEN)

supported_skills = ["People skills", "Coding", "Cooking", "Languages"]

def gen_markup_rows(rows):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for row in rows:
        markup.add(InlineKeyboardButton(row, callback_data=row))
    return markup

def gen_markup_for_delete(rows):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for row in rows:
        markup.add(InlineKeyboardButton(row, callback_data=row+"del"))
    return markup


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
    # MAKE THIS A CALLBACK QUERY WITH AN InlineKeyboard AND ADD THE SKILL TO THE USER
    markup = gen_markup_rows(supported_skills)
    bot.send_message(message.chat.id, "Here are all the currently supported skills. Select which ones you possess!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def add_selected_skill_to_user(call : CallbackQuery):
    skill = call.data
    userlist = manager.get_users()
    cur_user = call.from_user.username


    # Check if the user is regsitered
    if cur_user not in userlist:
        bot.answer_callback_query(call.id, "You are not yet registered in our database! Use /register to be able to use the command.")


    # Check if it's a callback to delete the skill
    if skill[-3:] == "del":
        bot.answer_callback_query(call.id, f"Selected skill: {skill[-3:]}\nDeleting it from the database...")
        manager.delete_skill(skill, cur_user)
        time.sleep(1)
        bot.send_message(call.message.chat.id, "Skill succesfully deleted!")
    # If not, add the skill
    else:
        bot.answer_callback_query(call.id,f"Selected skill: {skill}\nAdding it to the database...")
        manager.insert_skill(skill, cur_user)
        bot.send_message(call.message.chat.id, "Skill succesfully deleted!")


@bot.message_handler(commands=['delete'])
def adding_user_skills(message):
    # MAKE THIS A CALLBACK QUERY WITH AN InlineKeyboard AND ADD THE SKILL TO THE USER
    cur_user = message.from_user.username
    userlist = manager.get_users()

    # Check if the user is in the database
    if cur_user not in userlist:
        bot.send_message(message.chat.id, "You are not yet registered in our database! Use /register to be able to use the command.")
        return

    # See if the user has any skills added
    cur_user_skills = manager.select_user_skills(cur_user)
    if not cur_user_skills:
        bot.send_message(message.chat.id, "You got no skills added yet! Do /add to add some new skills!")
        return

    user_skills = manager.select_user_skills(cur_user)
    skills = []
    print(user_skills)
    for i in range(len(user_skills)):
        skills += [user_skills[i][0]]
    markup = gen_markup_for_delete(skills)
    bot.send_message(message.chat.id, "Here are all the skills you have. Select which one you'd like to delete!", reply_markup=markup)

@bot.message_handler(commands=['show'])
def show_user_skills(message):
    cur_user = message.from_user.username
    userlist = manager.get_users()
    # Check if the user is found in the database
    if cur_user not in userlist:
        bot.send_message(message.chat.id, "You are not yet registered! Go use /register so that you can use the rest of the commands.")
        return
    skills = manager.select_user_skills(cur_user)
    # Check if the user has any recorded skills
    if not skills:
        bot.send_message(message.chat.id, "You haven't got any skills added yet! Pick a skill you're good at using /add")
        return
    skills = [i for sub in skills for i in sub] # Found this neat oneliner to combine a list of tuples into a single list
    skills = ", ".join(skills) # Join the list with all the skills of the user
    bot.send_message(message.chat.id, f"Here are all your current skills: {skills}")
    



@bot.message_handler(commands=['job', 'proffession'])
def give_job_recommendation(message):
    cur_user = message.from_user.username
    userlist = manager.get_users()


    # Check if the user is found in the database
    if cur_user not in userlist:
        bot.send_message(message.chat.id, "You are not yet registered! Go use /register so that you can use the rest of the commands.")
        return
    skills = manager.select_user_skills(cur_user)
    # Check if the user has any recorded skills
    if not skills:
        bot.send_message(message.chat.id, "You haven't got any skills added yet! Pick a skill you're good at using /add")
        return
    
    stringslist = manager.select_based_on_skills(cur_user)
    stringslist = "\n".join(stringslist)
    bot.send_message(message.chat.id, "Here are all the jobs we have found for you based on your skills!\n\n" + stringslist + "\n\nIf you want to check out what your current skills are, type /show")


@bot.message_handler(commands=['help'])
def show_help(message):
    all_skills = ", ".join(supported_skills)
    help_text = (
        "🛠 **Bot Help Menu**\n\n"
        "Here's what I can help you with:\n\n"
        "👉 /start - Start talking to me\n"
        "👉 /register - Register yourself so I can remember you\n"
        "👉 /add - Add skills you’re good at\n"
        "👉 /delete - Delete skills you no longer want listed\n"
        "👉 /show - Show your currently saved skills\n"
        "👉 /job or /proffession - Get job suggestions based on your skills\n"
        "👉 /help - Show this message again anytime\n\n"
        f"🧠 Supported skills: {all_skills}\n"
        "🔁 Use buttons to add or delete skills via inline menus.\n"
        "\nNeed more help? Just ask!"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


keywords = {
    "Developer" : ["coding", "code", "languages", "culture"],
    "Cook" : ["cooking", "food"],
    "Nurse" : ["med", "medicine", "doctor", "nursing","care","healthcare"],
    "Teacher" : ["kids","teaching","sub",],
    "Translator" : ["language"]
}

@bot.message_handler(func=lambda message: True)
def bot_catching_keywords(message):
    text = str(message.text).lower()
    print(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Replace special characters with empty spaces
    message_parts = text.split() # Split the message into parts to look for keywords
    print(text)
    print(message_parts)
    

    # To catch the keywords for later
    caught = []
    
    for jobs, keyword in keywords.items(): # Look through every item in the dictionary
        # Iterate through every word user sent
        print("Iterating...")
        print(f"{jobs}\n--------\n{keyword}")
        for word in message_parts:
            # Check if the word is in the dictionary
            print("the word is: "+word)
            print(caught)
            if word in keyword:
                # If yes, add it to the list
                caught.append((word,jobs))

    # Check if we caught anything at all
    if not caught:
        bot.send_message(message.chat.id, "Heya! I noticed you typing stuff in chat. Do /register to be able to use commands, or do /help if you don't know what I can do.")
        return

    for keyword, job in caught:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        bot.send_message(message.chat.id, f"I caught the word '{keyword}', I think that would fit someone like {job}")



if __name__ == "__main__":
    manager = Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()

    bot.delete_webhook()
    bot.infinity_polling()