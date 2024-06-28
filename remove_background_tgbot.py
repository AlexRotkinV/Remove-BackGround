# -*- coding: windows-1251 -*-
from aiogram.utils.markdown import hlink
import rembg 
from PIL import Image
import telebot
from telebot import types
import os

bot = telebot.TeleBot("7106432490:AAHmEAiI_U13avLmvDm7taHW6tXbAX_GvAM")

link = hlink("Алексей Роткин", "https://t.me/akexrotkin_prog")
title = f"""
Привет! Пришли мне фото, а я уберу из неё фон и отправлю тебе в PNG.
    
Бот разработал {link}
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
        markup.add(types.InlineKeyboardButton("Канал автора", url="https://t.me/akexrotkin_prog"))
        bot.send_photo(message.chat.id, photo, caption=title, reply_markup=markup, parse_mode="HTML")

    @bot.message_handler()
    def text(message):
        bot.send_message(message.chat.id, "Пришли мне фото!")

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