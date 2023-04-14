from telebot import types
import telebot
from database import Database


my_user_id = 368195441
bot = telebot.TeleBot("5647871316:AAEsxZI1piQcqhp9LO0TA7kzwI4NfQTfjLo")

db = Database('db.db')


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔎 Find a partner')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔗 Share your profile')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('❌ Stop searching')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🧔🏻‍♂️ Male')
    item2 = types.KeyboardButton('👱🏻‍♀️ Female')
    markup.add(item1, item2)

    bot.send_message(
        message.chat.id,
        f"😊 ___Hello {message.from_user.first_name}, welcome to anonymous chat!\n\nSelect your gender:___",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.message_handler(commands = ['support'])
def support(message):
    markup = types.InlineKeyboardMarkup()
    row1 = [types.InlineKeyboardButton('PayPal 🪪',
                                       url='https://paypal.me/mirabbosdev'),
            types.InlineKeyboardButton('Revolut 💳',
                                       url='https://revolut.me/mirabbos')]
    row2 = [types.InlineKeyboardButton('Contact 👨🏻‍💻',
                                       url='https://t.me/mirabbos_developer')]
    markup.row(*row1)
    markup.row(*row2)

    bot.send_message(
        message.chat.id,
        f"😊 ___Thank you {message.from_user.first_name} for your interest in helping this project!\n\nYour support is greatly appreciated. Thank you for helping us make this project a success 🚀___",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Next ➡️')
    markup.add(item1)

    if chat_info != False:
        db.delete_chat(chat_info[0])
        bot.send_message(chat_info[1], '😢 ___Your partner has ended the chat___', reply_markup=markup, parse_mode='Markdown')
        bot.send_message(message.chat.id, '👋 ___You left the chat___', reply_markup=markup, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, '😐 ___You have no active chats right now___', reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['check'])
def check_chat(message):
    if message.chat.id == my_user_id:
        chats_info = db.check_chats()
        bot.send_message(my_user_id, text=f"Current chats {chats_info}:\n\n{chats_info}")

@bot.message_handler(content_types= ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🔎 Find a partner' or message.text == 'Next ➡️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🔎 Male')
            item2 = types.KeyboardButton('👫 Random')
            item3 = types.KeyboardButton('🔎 Female')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, '😊 ___Who do you want to search?___', reply_markup=markup, parse_mode='Markdown')

        elif message.text == '❌ Stop searching':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '💔 ___Search has been stopped___', reply_markup=main_menu(), parse_mode='Markdown')

        elif message.text == '🔎 Male':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:

                if db.add_queue(message.chat.id, db.get_gender(message.chat.id)) == False:
                    # if user already has a partner
                    bot.send_message(message.chat.id, '___🙄 You are chatting now...___', reply_markup=stop_dialog(), parse_mode='Markdown')
                else:
                    bot.send_message(message.chat.id, '🕵️ ___Looking for a male partner…___', reply_markup=stop_search(), parse_mode='Markdown')
            else:
                mess = f"🎉 ___Partner found! Say hi!___ 😊"

                bot.send_message(message.chat.id, mess, reply_markup=stop_dialog(), parse_mode='Markdown')
                bot.send_message(chat_two, mess, reply_markup=stop_dialog(), parse_mode='Markdown')


        elif message.text == '🔎 Female':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                if db.add_queue(message.chat.id, db.get_gender(message.chat.id)) == False:
                    # if user already has a partner
                    bot.send_message(message.chat.id, '___🙄 You are chatting now...___', reply_markup=stop_dialog(), parse_mode='Markdown')
                else:
                    bot.send_message(message.chat.id, '🕵️ ___Looking for a female partner…___', reply_markup=stop_search(), parse_mode='Markdown')
            else:
                mess = f"🎉 ___Partner found! Say hi!___ 😊"

                bot.send_message(message.chat.id, mess, reply_markup=stop_dialog(), parse_mode='Markdown')
                bot.send_message(chat_two, mess, reply_markup=stop_dialog(), parse_mode='Markdown')


        elif message.text == '👫 Random':
            user_info = db.get_chat()
            chat_two = user_info[0] # берем собеседника который стоит на очереди

            if db.create_chat(message.chat.id, chat_two) == False:
                if db.add_queue(message.chat.id, db.get_gender(message.chat.id)) == False:
                    # if user already has a partner
                    bot.send_message(message.chat.id, '___🙄 You are chatting now...___', reply_markup=stop_dialog(), parse_mode='Markdown')
                else:
                    bot.send_message(message.chat.id, '🕵️ ___Looking for a random partner…___', reply_markup=stop_search(), parse_mode='Markdown')
            else:
                mess = f"🎉 ___Partner found! Say hi!___ 😊"

                bot.send_message(message.chat.id, mess, reply_markup=stop_dialog(), parse_mode='Markdown')
                bot.send_message(chat_two, mess, reply_markup=stop_dialog(), parse_mode='Markdown')

        elif message.text == '🔗 Share your profile':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🙈 ___You have shared your profile___', parse_mode='Markdown')
                else:
                    bot.send_message(message.chat.id, '❌ ___You have not set a username___', parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, '😐 ___You have no active chats right now___', parse_mode='Markdown')


        elif message.text == '🧔🏻‍♂️ Male':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ ___Your gender was successfully added___', reply_markup=main_menu(), parse_mode='Markdown')
                bot.send_message(my_user_id, f'Joined: @{message.from_user.username} | {db.get_gender(message.chat.id)} | {message.chat.id}')
            else:
                bot.send_message(message.chat.id, '❌ <em>You already set your gender, please contact <a href="https://t.me/mirabbos_developer">Admin</a> to change it</em>',parse_mode='HTML', reply_markup=main_menu(), disable_web_page_preview=True)
                bot.send_message(my_user_id,
                                 f'Joined: @{message.from_user.first_name} | {db.get_gender(message.chat.id)} | {message.chat.id}')


        elif message.text == '👱🏻‍♀️ Female':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ ___Your gender was successfully added___', reply_markup=main_menu(), parse_mode='Markdown')
                bot.send_message(my_user_id,
                                 f'Joined: @{message.from_user.username} | {db.get_gender(message.chat.id)} | {message.chat.id}')
            else:
                bot.send_message(message.chat.id, '❌ <em>You already set your gender, please contact <a href="https://t.me/mirabbos_developer">Admin</a> to change it</em>',parse_mode='HTML', reply_markup=main_menu(), disable_web_page_preview=True)
                bot.send_message(my_user_id,
                                 f'Joined: @{message.from_user.first_name} | {db.get_gender(message.chat.id)} | {message.chat.id}')

        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)

            else:
                bot.send_message(message.chat.id, '😐 ___You have no active chats right now___', parse_mode='Markdown', reply_markup=main_menu())


######################
# MEDIA SECTION
######################

# Sending Sticker
@bot.message_handler(content_types='sticker')
def bot_sticker(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id,'😐 ___You have no active chats right now___', parse_mode='Markdown')

# Sending Voice
@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
            bot.send_voice(my_user_id, message.voice.file_id)
        else:
            bot.send_message(message.chat.id,'😐 ___You have no active chats right now___', parse_mode='Markdown')

# Sending Photo
@bot.message_handler(content_types='photo')
def bot_photo(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            photo_id = message.photo[-1].file_id
            caption = message.caption
            if caption:
                bot.send_photo(chat_info[1], photo_id, caption=caption)
                bot.send_photo(my_user_id, photo_id, caption=caption)
            else:
                bot.send_photo(chat_info[1], photo_id)
                bot.send_photo(my_user_id, photo_id)
        else:
            bot.send_message(message.chat.id,'😐 ___You have no active chats right now___', parse_mode='Markdown')

# Sending Video
@bot.message_handler(content_types='video')
def bot_video(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            video_id = message.video[-1].file_id
            caption = message.caption
            if caption:
                bot.send_video(chat_info[1], video_id, caption=caption)
                bot.send_video(my_user_id, video_id, caption=caption)
            else:
                bot.send_video(chat_info[1], video_id)
                bot.send_video(my_user_id, video_id)
        else:
            bot.send_message(message.chat.id,'😐 ___You have no active chats right now___', parse_mode='Markdown')

# Sending Animation
@bot.message_handler(content_types='animation')
def bot_animation(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            animation_id = message.animation[-1].file_id
            caption = message.caption
            if caption:
                bot.send_animation(chat_info[1], animation_id, caption=caption)
                bot.send_animation(my_user_id, animation_id, caption=caption)
            else:
                bot.send_animation(chat_info[1], animation_id)
                bot.send_animation(my_user_id, animation_id)
        else:
            bot.send_message(message.chat.id,'😐 ___You have no active chats right now___', parse_mode='Markdown')


print('Bot is live now')
bot.polling(none_stop = True)
