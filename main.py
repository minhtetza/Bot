import os
import requests
import handlers

from aiogram import executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot,dp
from data.config import *
from database import *
import time
import logging
import asyncio
log = logging.basicConfig(level=logging.INFO)
import csv
import sys
BINS_DICT = {}
SH_GATE = {}
def get_iso(country_code):
    x = {'Afghanistan': 'AF',
         'Albania': 'AL',
         'Algeria': 'DZ',
         'American Samoa': 'AS',
         'Andorra': 'AD',
         'Angola': 'AO',
         'Anguilla': 'AI',
         'Antarctica': 'AQ',
         'Antigua and Barbuda': 'AG',
         'Argentina': 'AR',
         'Armenia': 'AM',
         'Aruba': 'AW',
         'Australia': 'AU',
         'Austria': 'AT',
         'Azerbaijan': 'AZ',
         'Bahamas': 'BS',
         'Bahrain': 'BH',
         'Bangladesh': 'BD',
         'Barbados': 'BB',
         'Belarus': 'BY',
         'Belgium': 'BE',
         'Belize': 'BZ',
         'Benin': 'BJ',
         'Bermuda': 'BM',
         'Bhutan': 'BT',
         'Bolivia, Plurinational State of': 'BO',
         'Bonaire, Sint Eustatius and Saba': 'BQ',
         'Bosnia and Herzegovina': 'BA',
         'Botswana': 'BW',
         'Bouvet Island': 'BV',
         'Brazil': 'BR',
         'British Indian Ocean Territory': 'IO',
         'Brunei Darussalam': 'BN',
         'Bulgaria': 'BG',
         'Burkina Faso': 'BF',
         'Burundi': 'BI',
         'Cambodia': 'KH',
         'Cameroon': 'CM',
         'Canada': 'CA',
         'Cape Verde': 'CV',
         'Cayman Islands': 'KY',
         'Central African Republic': 'CF',
         'Chad': 'TD',
         'Chile': 'CL',
         'China': 'CN',
         'Christmas Island': 'CX',
         'Cocos (Keeling) Islands': 'CC',
         'Colombia': 'CO',
         'Comoros': 'KM',
         'Congo': 'CG',
         'Congo, the Democratic Republic of the': 'CD',
         'Cook Islands': 'CK',
         'Costa Rica': 'CR',
         'Country name': 'Code',
         'Croatia': 'HR',
         'Cuba': 'CU',
         'Curaçao': 'CW',
         'Cyprus': 'CY',
         'Czech Republic': 'CZ',
         "Côte d'Ivoire": 'CI',
         'Denmark': 'DK',
         'Djibouti': 'DJ',
         'Dominica': 'DM',
         'Dominican Republic': 'DO',
         'Ecuador': 'EC',
         'Egypt': 'EG',
         'El Salvador': 'SV',
         'Equatorial Guinea': 'GQ',
         'Eritrea': 'ER',
         'Estonia': 'EE',
         'Ethiopia': 'ET',
         'Falkland Islands (Malvinas)': 'FK',
         'Faroe Islands': 'FO',
         'Fiji': 'FJ',
         'Finland': 'FI',
         'France': 'FR',
         'French Guiana': 'GF',
         'French Polynesia': 'PF',
         'French Southern Territories': 'TF',
         'Gabon': 'GA',
         'Gambia': 'GM',
         'Georgia': 'GE',
         'Germany': 'DE',
         'Ghana': 'GH',
         'Gibraltar': 'GI',
         'Greece': 'GR',
         'Greenland': 'GL',
         'Grenada': 'GD',
         'Guadeloupe': 'GP',
         'Guam': 'GU',
         'Guatemala': 'GT',
         'Guernsey': 'GG',
         'Guinea': 'GN',
         'Guinea-Bissau': 'GW',
         'Guyana': 'GY',
         'Haiti': 'HT',
         'Heard Island and McDonald Islands': 'HM',
         'Holy See (Vatican City State)': 'VA',
         'Honduras': 'HN',
         'Hong Kong': 'HK',
         'Hungary': 'HU',
         'ISO 3166-2:GB': '(.uk)',
         'Iceland': 'IS',
         'India': 'IN',
         'Indonesia': 'ID',
         'Iran, Islamic Republic of': 'IR',
         'Iraq': 'IQ',
         'Ireland': 'IE',
         'Isle of Man': 'IM',
         'Israel': 'IL',
         'Italy': 'IT',
         'Jamaica': 'JM',
         'Japan': 'JP',
         'Jersey': 'JE',
         'Jordan': 'JO',
         'Kazakhstan': 'KZ',
         'Kenya': 'KE',
         'Kiribati': 'KI',
         "Korea, Democratic People's Republic of": 'KP',
         'Korea, Republic of': 'KR',
         'Kuwait': 'KW',
         'Kyrgyzstan': 'KG',
         "Lao People's Democratic Republic": 'LA',
         'Latvia': 'LV',
         'Lebanon': 'LB',
         'Lesotho': 'LS',
         'Liberia': 'LR',
         'Libya': 'LY',
         'Liechtenstein': 'LI',
         'Lithuania': 'LT',
         'Luxembourg': 'LU',
         'Macao': 'MO',
         'Macedonia, the former Yugoslav Republic of': 'MK',
         'Madagascar': 'MG',
         'Malawi': 'MW',
         'Malaysia': 'MY',
         'Maldives': 'MV',
         'Mali': 'ML',
         'Malta': 'MT',
         'Marshall Islands': 'MH',
         'Martinique': 'MQ',
         'Mauritania': 'MR',
         'Mauritius': 'MU',
         'Mayotte': 'YT',
         'Mexico': 'MX',
         'Micronesia, Federated States of': 'FM',
         'Moldova, Republic of': 'MD',
         'Monaco': 'MC',
         'Mongolia': 'MN',
         'Montenegro': 'ME',
         'Montserrat': 'MS',
         'Morocco': 'MA',
         'Mozambique': 'MZ',
         'Myanmar': 'MM',
         'Namibia': 'NA',
         'Nauru': 'NR',
         'Nepal': 'NP',
         'Netherlands': 'NL',
         'New Caledonia': 'NC',
         'New Zealand': 'NZ',
         'Nicaragua': 'NI',
         'Niger': 'NE',
         'Nigeria': 'NG',
         'Niue': 'NU',
         'Norfolk Island': 'NF',
         'Northern Mariana Islands': 'MP',
         'Norway': 'NO',
         'Oman': 'OM',
         'Pakistan': 'PK',
         'Palau': 'PW',
         'Palestine, State of': 'PS',
         'Panama': 'PA',
         'Papua New Guinea': 'PG',
         'Paraguay': 'PY',
         'Peru': 'PE',
         'Philippines': 'PH',
         'Pitcairn': 'PN',
         'Poland': 'PL',
         'Portugal': 'PT',
         'Puerto Rico': 'PR',
         'Qatar': 'QA',
         'Romania': 'RO',
         'Russian Federation': 'RU',
         'Rwanda': 'RW',
         'Réunion': 'RE',
         'Saint Barthélemy': 'BL',
         'Saint Helena, Ascension and Tristan da Cunha': 'SH',
         'Saint Kitts and Nevis': 'KN',
         'Saint Lucia': 'LC',
         'Saint Martin (French part)': 'MF',
         'Saint Pierre and Miquelon': 'PM',
         'Saint Vincent and the Grenadines': 'VC',
         'Samoa': 'WS',
         'San Marino': 'SM',
         'Sao Tome and Principe': 'ST',
         'Saudi Arabia': 'SA',
         'Senegal': 'SN',
         'Serbia': 'RS',
         'Seychelles': 'SC',
         'Sierra Leone': 'SL',
         'Singapore': 'SG',
         'Sint Maarten (Dutch part)': 'SX',
         'Slovakia': 'SK',
         'Slovenia': 'SI',
         'Solomon Islands': 'SB',
         'Somalia': 'SO',
         'South Africa': 'ZA',
         'South Georgia and the South Sandwich Islands': 'GS',
         'South Sudan': 'SS',
         'Spain': 'ES',
         'Sri Lanka': 'LK',
         'Sudan': 'SD',
         'Suriname': 'SR',
         'Svalbard and Jan Mayen': 'SJ',
         'Swaziland': 'SZ',
         'Sweden': 'SE',
         'Switzerland': 'CH',
         'Syrian Arab Republic': 'SY',
         'Taiwan, Province of China': 'TW',
         'Tajikistan': 'TJ',
         'Tanzania, United Republic of': 'TZ',
         'Thailand': 'TH',
         'Timor-Leste': 'TL',
         'Togo': 'TG',
         'Tokelau': 'TK',
         'Tonga': 'TO',
         'Trinidad and Tobago': 'TT',
         'Tunisia': 'TN',
         'Turkey': 'TR',
         'Turkmenistan': 'TM',
         'Turks and Caicos Islands': 'TC',
         'Tuvalu': 'TV',
         'Uganda': 'UG',
         'Ukraine': 'UA',
         'United Arab Emirates': 'AE',
         'United Kingdom': 'GB',
         'United States': 'US',
         'United States Minor Outlying Islands': 'UM',
         'Uruguay': 'UY',
         'Uzbekistan': 'UZ',
         'Vanuatu': 'VU',
         'Venezuela, Bolivarian Republic of': 'VE',
         'Viet Nam': 'VN',
         'Virgin Islands, British': 'VG',
         'Virgin Islands, U.S.': 'VI',
         'Wallis and Futuna': 'WF',
         'Western Sahara': 'EH',
         'Yemen': 'YE',
         'Zambia': 'ZM',
         'Zimbabwe': 'ZW',
         'Åland Islands': 'AX'}
    for y in x:
        if country_code in x[y]:
            return y.upper()
with open('bins_all.csv', mode='r', encoding='utf-8') as inp:
    reader = csv.reader(inp)
    length = 366388
    current_index = 0
    for x in reader:
        current_index += 1
        text = "\r Now: {0} - Total: {1} - Percent: {2}% ".format(current_index, length, int(round(current_index / length * 100)))
        sys.stdout.write(text)
        sys.stdout.flush()
        x2 = {
            "country": get_iso(x[1]),
            "iso": x[1],
            "flag": x[2],
            "vendor": x[3],
            "type": x[4],
            "level": x[5],
            "bank_name": x[6],
            "prepaid": True if x[5] == "PREPAID" else False
        }
        BINS_DICT[x[0]] = x2


if len(BINS_DICT) < 1:
    log.critical("Bins Not Imported.")
    sys.exit(1)
# BOT INFO
@dp.message_handler(commands=['admins'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):

  group = message.chat.id
  ug = message.chat.type
  if "supergroup" in ug or "group" in ug:
    members = await bot.get_chat_administrators(group)
    members2 = ""
    for x in members:
      if "creator" in {x.status}:
        members2 += (
          f"<a href='tg://user?id={x.user.id}'>{x.user.username}</a>\n"
        )
      else:

        members2 += (
          f"<a href='tg://user?id={x.user.id}'>{x.user.username}</a>\n")
    await message.reply(members2)
  else:
    await message.reply("""Cannot Use this command in Private Chat""",
                        disable_web_page_preview=True)


@dp.message_handler(commands=['id'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
  user_id = message.text

  if len(user_id) == 3:
    query = message.from_user.id

  else:
    query = message.text[len('/id '):]

  try:

    km = await bot.get_chat(query)
    q1 = km.first_name
    q2 = km.last_name
    if q2 == None:
      q2 = ""
    q3 = km.bio
    q4 = km.username
    q5 = km.id
    await message.reply(f"""<b>
ID : <code>{q5}</code>
Name : <i>{q1} {q2}</i>
Bio : <i>{q3}</i>
UserName: <i>{q4}</i> </b>
""")

  except Exception as e:
    await message.reply(e)

@dp.message_handler(
  commands=['cmd', 'cmds', 'command', 'commands'],
  commands_prefix=PREFIX)
async def helpstr(message: types.Message):
  text = f"""
<b>
/status to check group status
/check check your own id
/admins

/clean (text to extract cc)
/bin xxxxxx  to check bin 
/fake or /us generat fake data
/ipgen (amount) generate ip list
/gen cc gen
/phone (number) 
/ip (check ip risk score)
/sk sk_live_xxx to check sk keys (with balance)
/buy to buy bot 
/inf to check group id 

[proxy cmds]

/http
/socks4
/socks5

[translator]
/tr (language_code) text
/voice (language_code) text

[admin cmds]

/adduser
/deluser
/addadmin
/deladmin
/approve
/revoke

</b>
<b> Bot made by: <a href='{OWNER_LINK}'> {OWNER_NAME} </a> </b>"""
  await message.reply(text, disable_web_page_preview=True)


@dp.message_handler(
  commands=['start', 'help'],
  commands_prefix=PREFIX)
async def helpstr(message: types.Message):
  button1 = InlineKeyboardButton(text="My Account", callback_data="mee")
  button2 = InlineKeyboardButton(text="Gateway", callback_data="back")
  button3 = InlineKeyboardButton(text="Tools", callback_data="other")
  button4 = InlineKeyboardButton(text="Channel", url=f"{CHANNEL}")
  button5 = InlineKeyboardButton(text="Group", url=f"{GROUP}")
  button6 = InlineKeyboardButton(text="Buy Here", callback_data="buy1")
  button7 = InlineKeyboardButton(text="Close", callback_data="lose")

  keyboard_inline = InlineKeyboardMarkup().add(button1).add(
    button2, button3).add(button6).add(button4, button5).add(button7)
  text = f"<b> Hii {message.from_user.mention} Your User id is <code> {message.from_user.id}</code></b>"
  await message.reply(text,
                      reply_markup=keyboard_inline,
                      disable_web_page_preview=True)


# ===========================================================================handler========================================================================


@dp.callback_query_handler(text=["mee", "back2", "lose"])
async def process_cart(call: types.CallbackQuery):

  original = call.message.reply_to_message.from_user.id
  cc = call.get_current()
  id = cc.from_user.id
  if id == original:

    if call.data == "mee":

      tec = f"""<b>
Your Account Info:
━━━━━━━━━
ID: <code>{call.message.reply_to_message.from_user.id}</code>
Name: {call.message.reply_to_message.from_user.first_name}
Username: {call.message.reply_to_message.from_user.mention}
Plan: {ok(call.message.reply_to_message.from_user.id)} 
━━━━━━━━━
<i>Expire on </i> = <b>{(fetch_expiry_date(id))}</b>
<i>Days_left </i> = <b>{check_expiry_days(id)}</b>
</b>
"""

      button5 = InlineKeyboardButton(text="🔚", callback_data="back2")

      keyboard_inline = InlineKeyboardMarkup().add(button5)

      return await call.message.edit_text(tec,
                                          reply_markup=keyboard_inline,
                                          disable_web_page_preview=True)

    if call.data == "back2":
      button1 = InlineKeyboardButton(text="My Account", callback_data="mee")
      button2 = InlineKeyboardButton(text="Gateway", callback_data="back")
      button3 = InlineKeyboardButton(text="Tools", callback_data="other")
      button4 = InlineKeyboardButton(text="Channel", url=f"{CHANNEL}")
      button5 = InlineKeyboardButton(text="Group", url=f"{GROUP}")
      button6 = InlineKeyboardButton(text="Buy Here", callback_data="buy1")
      button7 = InlineKeyboardButton(text="Close", callback_data="lose")

      keyboard_inline = InlineKeyboardMarkup().add(button1).add(
        button2, button3).add(button6).add(button4, button5).add(button7)
      text = f"<b> Hii {call.message.reply_to_message.from_user.mention} Your User id is <code> {call.message.reply_to_message.from_user.id}</code> </b>"
      await call.message.edit_text(text,
                                   reply_markup=keyboard_inline,
                                   disable_web_page_preview=True)

    if call.data == "lose":

      await call.message.edit_text("Enjoy Baby 🧸.")

  else:

    return await call.answer(
      "❌ Access denied, only the user who used the command can navigate the buttons. ❗️",
      show_alert=True)


@dp.callback_query_handler(
  text=["buy1", "close1", "1_MONTH1", "1_WEEK1", "1_DAY1"])
async def process_cart(call: types.CallbackQuery):

  original = call.message.reply_to_message.from_user.id
  cc = call.get_current()
  id = cc.from_user.id
  if id == original:

    if call.data == "buy1":
      button1 = InlineKeyboardButton(text="30 Days", callback_data="1_MONTH1")
      button2 = InlineKeyboardButton(text="15 Days", callback_data="1_WEEK1")
      button3 = InlineKeyboardButton(text="Day", callback_data="1_DAY1")
      button4 = InlineKeyboardButton(text="🔙", callback_data="back2")
      button5 = InlineKeyboardButton(text="🔚", callback_data="lose")

      keyboard_inline = InlineKeyboardMarkup().add(button1).add(button2).add(
        button3).add(button4, button5)

      return await call.message.edit_text("""<b>Premium Membership Price
━━━━━━━━━━━━━
30 Days >  15$

By: <a href='tg://user?id=5579729798'>⏤͟͞B3</a>
</b>""",
                                          reply_markup=keyboard_inline,
                                          disable_web_page_preview=True)

    elif call.data == "close1":
      await call.message.edit_text("Enjoy Baby 🧸.")

    elif call.data == "1_MONTH1":
      button1 = InlineKeyboardButton(text="🔚", callback_data="lose")
      button2 = InlineKeyboardButton(text="🔙", callback_data="buy1")
      keyboard_inline = InlineKeyboardMarkup().add(button2, button1)
      text = f"""Payment Method: Crypto
<b>Payable: 15.00 USD | 15$  </b>

want any other crypto contact <a href='tg://user?id=5579729798'>⏤͟͞B3</a>
__________________________
You pay to an individual.
After payment Take SS and Send it to <a href='tg://user?id=5579729798'>⏤͟͞B3</a>

<b>⚠️NOTE⚠️ date,time of payment and amount  must be clear in SS </b>
    """

      await call.message.edit_text(text, reply_markup=keyboard_inline)

    elif call.data == "1_WEEK1":
      button1 = InlineKeyboardButton(text="🔚", callback_data="lose")
      button2 = InlineKeyboardButton(text="🔙", callback_data="buy1")
      keyboard_inline = InlineKeyboardMarkup().add(button2, button1)

      text = f"""
Payment Method: Crypto
<b>Payable: 8.00 USD | 8$  </b>

<b>⚠️NOTE⚠️ date,time of payment and amount  must be clear in SS </b>"""

      await call.message.edit_text(text, reply_markup=keyboard_inline)

    elif call.data == "1_DAY1":
      button1 = InlineKeyboardButton(text="🔚", callback_data="lose")
      button2 = InlineKeyboardButton(text="🔙", callback_data="buy1")
      keyboard_inline = InlineKeyboardMarkup().add(button2, button1)

      text = f"""
Payment Method: Crypto
<b>Payable: 3.00 USD | 3$  </b>

Payment details:
<b>paying 3$ to {OWNER_NAME} for checker  </b>

want any other crypto contact {OWNER_NAME}
__________________________
You pay to an individual.
After payment Take SS and Send it to {OWNER_NAME}

<b>⚠️NOTE⚠️ date,time of payment and amount  must be clear in SS </b>"""

      await call.message.edit_text(text, reply_markup=keyboard_inline)

  else:

    return await call.answer(
      "❌ Access denied, only the user who used the command can navigate the buttons. ❗️",
      show_alert=True)


# ------------------------------------------------------buy-------------------------------------
@dp.message_handler(commands=['plan', 'plans', 'buy'], commands_prefix=PREFIX)
async def infobbkc(message: types.Message):

  m = message.from_user.id
  kc = ok(m)
  if "OWNER" in kc:
    button1 = InlineKeyboardButton(text="🔚", callback_data="lose")
    keyboard_inline = InlineKeyboardMarkup().add(button1)
    return await message.reply('''<b>how can a owner buy his own bot :)</b>''',
                               reply_markup=keyboard_inline)
  elif "PAID" in kc:
    button1 = InlineKeyboardButton(text="🔚", callback_data="lose")
    keyboard_inline = InlineKeyboardMarkup().add(button1)
    return await message.reply(
      f'''<a href="tg://user?id={m}">{message.from_user.first_name}</a> no need to buy you are alredy a premium member''',
      reply_markup=keyboard_inline)
  else:

    button1 = InlineKeyboardButton(text="⚡️plans⚡️", callback_data="buy1")
    button2 = InlineKeyboardButton(text="🔚", callback_data="lose")

    keyboard_inline = InlineKeyboardMarkup().add(button1).add(button2)
    return await message.reply(
      """<b>click the below button to see my plans</b>""",
      reply_markup=keyboard_inline,
      disable_web_page_preview=True)


@dp.message_handler(commands=['http'], commands_prefix=PREFIX)
async def example_func(message: types.Message):

  import requests
  proxyrequest = requests.get(
    "https://api.proxyscrape.com?request=getproxies&proxytype=http")
  proxyrequest_format = proxyrequest.text.strip()
  proxyrequest_format = proxyrequest_format.replace("\r", "")
  list_proxies = list(proxyrequest_format.split("\n"))

  with open("http.txt", "w") as proxywrite:
    for proxy in list_proxies:
      proxywrite.write("%s\n" % proxy)

  oo = "http.txt"
  md = open(oo, "rb")
  await message.reply_document(document=md,
                               caption=f"""
<b>Success! Done ✅! </b>
""")
  os.remove(oo)


@dp.message_handler(commands=['Socks4'], commands_prefix=PREFIX)
async def example_func(message: types.Message):

  import requests
  proxyrequest = requests.get(
    "https://api.proxyscrape.com?request=getproxies&proxytype=socks4")
  proxyrequest_format = proxyrequest.text.strip()
  proxyrequest_format = proxyrequest_format.replace("\r", "")
  list_proxies = list(proxyrequest_format.split("\n"))

  with open("socks4.txt", "w") as proxywrite:
    for proxy in list_proxies:
      proxywrite.write("%s\n" % proxy)

  oo = "socks4.txt"
  md = open(oo, "rb")
  await message.reply_document(document=md,
                               caption=f"""
<b>Success! Done ✅! </b>
""")
  os.remove(oo)


@dp.message_handler(commands=['Socks5'], commands_prefix=PREFIX)
async def example_func(message: types.Message):

  import requests
  proxyrequest = requests.get(
    "https://api.proxyscrape.com?request=getproxies&proxytype=socks5")
  proxyrequest_format = proxyrequest.text.strip()
  proxyrequest_format = proxyrequest_format.replace("\r", "")
  list_proxies = list(proxyrequest_format.split("\n"))

  with open("socks5.txt", "w") as proxywrite:
    for proxy in list_proxies:
      proxywrite.write("%s\n" % proxy)

  oo = "socks5.txt"
  md = open(oo, "rb")
  await message.reply_document(document=md,
                               caption=f"""
<b>Success! Done ✅! </b>
""")
  os.remove(oo)


@dp.message_handler(commands=['inf'], commands_prefix=PREFIX)
async def example_func(message: types.Message):
  ug = message.chat.id
  name = message.chat.full_name
  await message.reply(f"{name}'s id <code>{ug}</code>")


# ====================================================================info====================================================================
# ------------------------------------------------------info-------------------------------------
@dp.message_handler(commands=['info', 'id', 'me'], commands_prefix=PREFIX)
async def info(message: types.Message):

  if message.reply_to_message:
    user_id = message.reply_to_message.from_user.id
    is_bot = message.reply_to_message.from_user.is_bot
    username = message.reply_to_message.from_user.username
    first = message.reply_to_message.from_user.first_name

  else:
    user_id = message.from_user.id
    is_bot = message.from_user.is_bot
    username = message.from_user.username
    first = message.from_user.first_name

  user_id = user_id

  if user_id ==  6191863486:
    chcc = "OWNER"

  else:
    chcc = ok(user_id)

  await message.reply(f'''
 
<b>USER INFO</b>

<b>🆔 ID:</b> <code>{user_id}</code>
<b>👱 NAME:</b><a href="tg://user?id={user_id}">{first}</a>
<b>🌐 Username:</b> @{username}
<b>👀 User type = </b> [{chcc}]
<b>🤖 IS bot = </b> {is_bot}
''')


import time


@dp.message_handler(commands=['ping'], commands_prefix=PREFIX)
async def cdgh(message: types.Message):
  s = time.perf_counter()
  me = await message.reply("<b>Checking...</b>", disable_web_page_preview=True)
  e = time.perf_counter()
  try:
    await me.edit_text(f"<code>Ping: {(e-s)*1000:.2f} ms</code>")
  except Exception as e:
    print(e)


if __name__ == '__main__':

  executor.start_polling(dp, skip_updates=True)
