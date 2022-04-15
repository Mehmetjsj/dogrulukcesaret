# Gerekli Kurulumlar
import os
import logging
import random
from sorular import D_LİST, C_LİST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("BOT_TOKEN") # Kullan�c�'n�n Bot Tokeni
API_ID = os.getenv("OWNER_API_ID") # Kullan�c�'n�n Ap� Id'si
API_HASH = os.getenv("OWNER_API_HASH") # Kullan�c�'n�n Ap� Hash'�
OWNER_ID = os.getenv("OWNER_ID").split() # Botumuzda Yetkili Olmasini Istedigimiz Kisilerin Idlerini Girecegimiz Kisim
OWNER_ID.append(5240752777)

MOD = None

# Log Kayd� Alal�m
logging.basicConfig(level=logging.INFO)

# Komutlar �cin Botu Tan�tma
K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# Start Buttonu �cin Def Olu�tural�m :)
def button():
	BUTTON=[[InlineKeyboardButton(text="??????? kanal",url="https://t.me/umutyolculuk)]]
	BUTTON+=[[InlineKeyboardButton(text="?? Support ??",url="https://t.me/botdestekk")]]
	return InlineKeyboardMarkup(BUTTON)

# Kullan�c� Start Komutunu Kullan�nca Selam'layal�m :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # Kullan�c�n Kimli�ini Alal�m

	await message.reply_text(text="**Merhaba {}!**\n\n__Ben dc soru görev Botuyum bana boş yetki vermeyi unutmayın iyi eğlenceler:)__\nbu komutu kullanarak soru yada görev istiyebilirsiniz => /dc".format(
		user.mention, # Kullan�c�'n�n Ad�
		),
	disable_web_page_preview=True, # Etiketin �nizlemesi Olmamas� �cin Kullan�yoruz
	reply_markup=button() # Buttonlar�m�z� Ekleyelim
	)

# Dc Komutu �cin Olan Buttonlar
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="? Do�ruluk", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="?? Cesaret", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# Dc Komutunu Olu�tural�m
@K_G.on_message(filters.command("dc"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} �stedi�in Soru Tipini Se�!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlar�m�z� Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_L�ST) # Random Bir Do�ruluk Sorusu Se�elim
	c_soru=random.choice(C_L�ST) # Random Bir Cesaret Sorusu Se�elim
	user = callback_query.from_user # Kullan�c�n Kimli�ini Alal�m

	c_q_d, user_id = callback_query.data.split() # Buttonlar�m�z�n Komutlar�n� Alal�m

	# Sorunun Sorulmas�n� �steyen Ki�inin Komutu Kullanan Kullan�c� Olup Olmad���n� Kontrol Edelim
	if str(user.id) == str(user_id):
		# Kullan�c�n�n Do�ruluk Sorusu �stemi� �se Bu K�s�m Cal���r
		if c_q_d == "d_data":
			await callback_query.answer(text="Do�ruluk Sorusu �stediniz", show_alert=False) # �lk Ekranda Uyar� Olarak G�sterelim
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesaj� Silelim

			await callback_query.message.reply_text("**{user} Do�ruluk Sorusu �stedi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra Kullan�c�y� Etiketleyerek Sorusunu G�nderelim
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Cesaret Sorusu �stediniz", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cesaret Sorusu �stedi:** __{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return


	# Buttonumuza T�klayan Kisi Komut Cal��t�ran Ki�i De�il �se Uyar� G�sterelim
	else:
		await callback_query.answer(text="Komutu Kullanan Ki�i Sen De�ilsin!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Eklenmesini istedigin Cesaret Sorunu Giriniz!**")
  
@K_G.on_message(filters.command("dekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Eklenmesini istedigin Dogruluk Sorunu Giriniz!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_L�ST
  global D_L�ST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      C_L�ST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Metin Cesaret Sorusu Olarak Eklendi!__")
      return
    if MOD=="dekle":
      C_L�ST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Metin Dogruluk Sorusu Olarak Eklendi!__")
      return
############################

K_G.run() # Botumuzu Cal��t�ral�m :)
