# -*- coding: windows-1251 -*-
from aiogram.utils.markdown import hlink
import rembg 
from PIL import Image
import telebot
from telebot import types
import os

bot = telebot.TeleBot("BOT_TOKEN")

link = hlink("Àëåêñåé Ðîòêèí", "https://t.me/akexrotkin_prog")
title = f"""
Ïðèâåò! Ïðèøëè ìíå ôîòî, à ÿ óáåðó èç íå¸ ôîí è îòïðàâëþ òåáå â PNG.
    
Áîò ðàçðàáîòàë {link}
    """

def remove_background(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    path_file = f"photos\{message.chat.id}"
    path_jpg = f"{path_file}\{message.id}.jpg"
    path_png = f"{path_file}\photo_{message.id}.png"    
 
    try:
        os.mkdir(path_file)
    except FileExistsError:
        pass
    
    with open(path_jpg, 'wb') as new_file:
        new_file.write(downloaded_file)
    output = rembg.remove(Image.open(path_jpg))
    output.save(path_png)
    bot.send_document(message.chat.id, open(path_png, 'rb'))
    
    os.remove(path_png)
    os.remove(path_jpg)
    try:
        os.rmdir(path_file)
    except OSError:
        pass
    
def main():
    @bot.message_handler(commands=["start"])
    def start(message):
        photo = open(os.path.join("photos", "cover.png"), 'rb')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Êàíàë àâòîðà", url="https://t.me/akexrotkin_prog"))
        bot.send_photo(message.chat.id, photo, caption=title, reply_markup=markup, parse_mode="HTML")

    @bot.message_handler()
    def text(message):
        bot.send_message(message.chat.id, "Ïðèøëè ìíå ôîòî!")

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        if message.chat.id != 992586773:
            bot.send_photo(chat_id=992586773, photo=message.photo[-1].file_id, caption=f"@{message.from_user.username}")
        remove_background(message)
        
    
if __name__ == "__main__":
    print("Bot is ready")  
    try:
        main()
    except:
        pass
    
bot.infinity_polling(timeout=10, long_polling_timeout=5)
