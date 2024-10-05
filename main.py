
import random
import datetime
import re
import requests
import json
import time
import telebot
import os
from genfun import gen_card
import asyncio
from telethon import TelegramClient
from telebot import types

current_year = datetime.datetime.now().year % 100
current_month = datetime.datetime.now().month

# 
bot_token = '7771888330:AAGTeKLD0ByMoXSXNA338BWjoJdDVW_qOUQ'
admin_id = '6191863486'  # 
api_id = '9615664'  # 
api_hash = '32a7dd931eea1c701e2da971216b61b1'  # 
phone_number = '+201153262807'  # 
cache_file = "bin_cache.json"
bot_working = True

if os.path.exists(cache_file):
    with open(cache_file, "r") as file:
        bin_cache = json.load(file)
else:
    bin_cache = {}

def save_cache():
    with open(cache_file, "w") as file:
        json.dump(bin_cache, file)

def generate_cards(bin, count, expiry_month=None, expiry_year=None, use_backticks=False):
    cards = set()
    while len(cards) < count:
        try:
            card_number = bin + str(random.randint(0, 10**(16-len(bin)-1) - 1)).zfill(16-len(bin))
            if luhn_check(card_number):
                expiry_date = generate_expiry_date(current_year, current_month, expiry_month, expiry_year)
                cvv = str(random.randint(0, 999)).zfill(3)
                card = f"{card_number}|{expiry_date['month']}|{expiry_date['year']}|{cvv}"
                if use_backticks:
                    card = f"`{card}`"
                cards.add(card)
        except ValueError:
            continue
    return list(cards)

def generate_expiry_date(current_year, current_month, expiry_month=None, expiry_year=None):
    month = str(expiry_month if expiry_month and expiry_month != 'xx' else random.randint(1, 12)).zfill(2)
    year = str(expiry_year if expiry_year and expiry_year != 'xx' else random.randint(current_year, current_year + 5)).zfill(2)
    if int(year) == current_year and int(month) < current_month:
        month = str(random.randint(current_month, 12)).zfill(2)
    return {"month": month, "year": year}

def luhn_check(number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def get_bin_info(bin):
    if bin in bin_cache:
        return bin_cache[bin]
    
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin[:6]}")
        response.raise_for_status()
        data = response.json()
        info = {
            "scheme": data.get("scheme", "").upper(),
            "type": data.get("type", "").upper(),
            "brand": data.get("brand", "").upper(),
            "bank": data.get("bank", {}).get("name", "").upper(),
            "country": data.get("country", {}).get("name", "").upper(),
            "emoji": data.get("country", {}).get("emoji", "")
        }
        bin_cache[bin] = info
        save_cache()
        return info
    except Exception as e:
        print(f"Error fetching BIN info: {e}")
        return {
            "scheme": "",
            "type": "",
            "brand": "",
            "bank": "",
            "country": "",
            "emoji": ""
        }

# تهيئة البوت
bot = telebot.TeleBot(bot_token, parse_mode='HTML')

async def get_last_messages(username, limit, bin=None):
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(username)
            messages = await client.get_messages(entity, limit=limit)

            matching_texts = []
            card_pattern = r'(\d{15,16})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{2,4})[^0-9]+([0-9]{3,4})'

            for message in messages:
                if message.text:
                    match = re.search(card_pattern, message.text)
                    if match:
                        formatted_text = f"{match.group(1)}|{match.group(2)}|{match.group(3)}|{match.group(4)}"
                        if bin is None or formatted_text.startswith(bin):
                            matching_texts.append(formatted_text)

            return "\n".join(matching_texts), entity.title
        except Exception as e:
            print(f"Error: {e}")
            return None, None

def save_to_file(text):
    if os.path.exists('Original_Scrap.txt'):
        os.remove('Original_Scrap.txt')
    with open('Original_Scrap.txt', 'w') as file:
        file.write(text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    welcome_message = (
        f"● Welcome, {name}!\n"
        "● Welcome to bot scrap cc\n\n"
        "● You can scrape from your username, ID, invitation link, or user chats\n"
        "● You can scrape from bank name or bin\n"
        "● You can scrape from more than one bank or bin, all you have to do is put ',' between them\n"
        "● for example: 12345,12345,12345,etc\n\n"
        "● The commands are below 🧸"
    )
    
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("≈ CC SCRAPPING FROM CHAT ≈", callback_data='scrap_from_chat')
    button2 = types.InlineKeyboardButton("≈ CC SCRAPPING FROM BIN ", callback_data='scrap_from_bin')
    button3 = types.InlineKeyboardButton("≈ SCRAPPE AMOUNT Bank Name", callback_data='scrap_amount_cc')
    
    button4 = types.InlineKeyboardButton("• Developer", url='https://t.me/Ownerxxxxx')
    button5 = types.InlineKeyboardButton("mass chk bot", url='https://t.me/GSIXTEAM_BOT')
    button6 = types.InlineKeyboardButton(" • Join Now", url='https://t.me/CHITNGE54')

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.row(button4, button5, button6)

    try:
        bot.send_message(message.chat.id, welcome_message, reply_markup=markup)  # بدون parse_mode='HTML'
    except Exception as e:
        print(f"Error sending welcome message: {e}")
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back(call):
    message_text = (
        "● Welcome to bot scrap cc\n"
        "● You can scrape from your username, ID, invitation link, or user chats\n"
        "● You can scrape from bank name or bin\n"
        "● You can scrape from more than one bank or bin, all you have to do is put ',' between them\n"
        "● for example: 12345,12345,12345,etc\n\n"
        "● The commands are below 🧸"
    )

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("≈ CC SCRAPPING FROM CHAT ≈", callback_data='scrap_from_chat')
    button2 = types.InlineKeyboardButton("≈ CC SCRAPPING FROM BIN ", callback_data='scrap_from_bin')
    button3 = types.InlineKeyboardButton("≈ SCRAPPE AMOUNT Bank Name ", callback_data='scrap_amount_cc')
    
    button4 = types.InlineKeyboardButton("• Developer", url='https://t.me/Ownerxxxxx')
    button5 = types.InlineKeyboardButton("mass chk bot", url='https://t.me/GSIXTEAM_BOT')
    button6 = types.InlineKeyboardButton(" • Join Now", url='https://t.me/CHITNGE54')

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.row(button4, button5, button6)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'scrap_from_chat')
def handle_scrap_from_chat(call):
    message_text = (
        "◎ CC SCRAPPING FROM CHAT\n"
        "• /scr USERNAME LIMIT\n"
        "⇾ EXAMPLE:\n"
        "    /scr CHITNGE54 500\n\n"
        "◎ CC SCRAPPING FROM BIN IN CHAT\n"
        "• /scr USERNAME BIN LIMIT\n"
        "⇾ EXAMPLE:\n"
        "    /scr CHITNGE54 500 440393\n"
        "    /scr CHITNGE54 500 440393,123456\n\n"
        "◎ CC SCRAPPING FROM Bank name IN CHAT\n"
        "• /scr USERNAME BIN LIMIT\n"
        "⇾ EXAMPLE:\n"
        "    /scr CHITNGE54 500 [JPMORGAN]\n"
        "    /scr CHITNGE54 500 [JPMORGAN,N.A]\n"
        "    \n\n"
        "Press Back to return."
    )
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Back", callback_data='back')
    markup.add(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'scrap_from_bin')
def handle_scrap_from_bin(call):
    message_text = (
        "◎ CC SCRAPPING FROM BIN IN ALL USER CHATS\n"
        "• /scr BIN,BIN\n"
        "⇾ EXAMPLE:\n"
        "    /scr 440393\n"
        "    /scr 440393,123456\n\n"
        "◎ CC SCRAPPING FROM Bank Name IN ALL USER CHATS\n"
        "• /scr [Bank]\n"
        "⇾ EXAMPLE:\n"
        "    /scr [JPMORGAN]\n"
        "    /scr [JPMORGAN,N.A]\n\n"
        "Press Back to return."
    )
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Back", callback_data='back')
    markup.add(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'scrap_amount_cc')
def handle_scrap_amount_cc(call):
    message_text = (
        "◎ SCRAPPE AMOUNT CC FROM Bank Name IN ALL USER CHATS\n"
        "• /scr [Bank]\n"
        "⇾ EXAMPLE:\n"
        "    /scr [JPMORGAN] 500\n"
        "    /scr [JPMORGAN,N.A] 500\n\n"
        "◎ SCRAPPE AMOUNT CC FROM BIN IN ALL USER CHATS\n"
        "• /scr [BIN]\n"
        "⇾ EXAMPLE:\n"
        "    /scr [440393] 500\n"
        "    /scr [440393,123456] 500\n\n"
        "Press Back to return."
    )
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Back", callback_data='back')
    markup.add(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'specific_chat':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You selected: SCRAPPING FROM Specific chat")
    elif call.data == 'all_user_chats':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You selected: SCRAPPING FROM ALL USER CHATS")
    elif call.data == 'amountcc':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You selected: SCRAPPE AMOUNTCC")

@bot.message_handler(commands=['scr'])
def send_sc_messages(message):
    chat_id = message.chat.id
    initial_message = bot.reply_to(message, "Scraping Started...⏳")
    command_parts = message.text.split()

    if len(command_parts) < 3:
        bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, 
                              text="Command format: /scr [username/bin] [limit]")
        return

    input_data = command_parts[1]
    limit = int(command_parts[2])

    if input_data.isdigit() and len(input_data) >= 6:  # نفترض أن البين يتكون من 6 أرقام على الأقل
        # سكرب من بين
        bin = input_data
        count = limit

        cards = generate_cards(bin, count)
        file_path = "Original_Scrap.txt"

        with open(file_path, "w") as file:
            file.write("\n".join(cards))

        bin_info = get_bin_info(bin[:6])

        additional_info = (f'''
            ●●●●●●●●●●●

• Name ~ Original Scraper 🧡, 

• Bin ~ {bin[:10]}\n

• Total Found ~ {count}\n

• Join Channel @CHITNGE54\n
●●●●●●●●●●●
        ''')

        with open(file_path, "rb") as file:
            bot.send_document(chat_id, file, caption=additional_info)
            bot.delete_message(chat_id=chat_id, message_id=initial_message.message_id)
    else:
        # سكرب من قناة
        username = input_data

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        messages_text, channel_name = loop.run_until_complete(get_last_messages(username, limit))

        if channel_name:
            save_to_file(messages_text)

            file_len = len(messages_text.split('\n')) if messages_text else 0
            captain_info = f"""
●●●●●●●●●●●

• Name ~ Original Scraper 🧡, 

• Channel ~ {channel_name}

• Total Found ~ {file_len}

• Join Channel @CHITNGE54

●●●●●●●●●●●"""

            with open('Original_Scrap.txt', 'rb') as file:
                markup = types.InlineKeyboardMarkup()
                
                dev_button = telebot.types.InlineKeyboardButton(text="𝗗𝗘𝗩", url='https://t.me/Ownerxxxxx')
                markup.add(dev_button)
                bot.send_document(chat_id, file, caption=captain_info, parse_mode='none', reply_markup=markup)
                bot.delete_message(chat_id=chat_id, message_id=initial_message.message_id)
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, 
                                  text="Failed to get messages from the channel.")

@bot.message_handler(commands=['gen'])
def generate_card(message):
    if bot_working:
        chat_id = message.chat.id
        try:
            initial_message = bot.reply_to(message, "Generating Started...⏳")
            card_info = message.text.split('/gen ', 1)[1]

            def multi_explode(delimiters, string):
                pattern = '|'.join(map(re.escape, delimiters))
                return re.split(pattern, string)
        
            split_values = multi_explode([":", "|", "⋙", " ", "/"], card_info)
            bin_value = ""
            mes_value = ""
            ano_value = ""
            cvv_value = ""
            
            if len(split_values) >= 1:
                bin_value = re.sub(r'[^0-9]', '', split_values[0])
            if len(split_values) >= 2:
                mes_value = re.sub(r'[^0-9]', '', split_values[1])
            if len(split_values) >= 3:
                ano_value = re.sub(r'[^0-9]', '', split_values[2])
            if len(split_values) >= 4:
                cvv_value = re.sub(r'[^0-9]', '', split_values[3])
                
            cards_data = ""
            f = 0
            while f < 10:
                card_number, exp_m, exp_y, cvv = gen_card(bin_value, mes_value, ano_value, cvv_value)
                cards_data += f"<code>{card_number}|{exp_m}|{exp_y}|{cvv}</code>\n"
                f += 1
                
            bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=cards_data, parse_mode='HTML')
        except Exception as e:
            bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=f"An error occurred: {e}")
    else:
        pass

bot.infinity_polling()
