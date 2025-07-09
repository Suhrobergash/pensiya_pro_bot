from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, CHANNELS

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 🌐 Til tanlash menyusi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🇺🇿 O‘zbek tili", "🇷🇺 Русский язык")
    await message.answer("Tilni tanlang 👇", reply_markup=keyboard)

# 📣 Kanalga obuna bo‘lganini tekshiruvchi funksiya
async def is_subscribed(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ("member", "creator", "administrator"):
                return False
        except:
            return False
    return True

# 🌐 Til tanlanganidan keyin ishlovchi handler
@dp.message_handler(lambda message: message.text in ["🇺🇿 O‘zbek tili", "🇷🇺 Русский язык"])
async def check_subscription(message: types.Message):
    subscribed = await is_subscribed(message.from_user.id)
    if not subscribed:
        buttons = types.InlineKeyboardMarkup(row_width=1)
        for ch in CHANNELS:
            buttons.add(types.InlineKeyboardButton(text=f"Kanalga a'zo bo'lish", url=f"https://t.me/{ch.replace('@','')}"))
        buttons.add(types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs"))
        await message.answer("Davom etish uchun quyidagi kanallarga a’zo bo‘ling:", reply_markup=buttons)
    else:
        await message.answer("Asosiy menyuga xush kelibsiz!")

# ✅ Tekshiruv tugmasi uchun callback
@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def check_callback(callback_query: types.CallbackQuery):
    subscribed = await is_subscribed(callback_query.from_user.id)
    if subscribed:
        await callback_query.message.edit_text("✅ Obuna tasdiqlandi! Menyuga o‘tamiz.")
    else:
        await callback_query.answer("❗ Hali hamma kanallarga obuna emassiz.", show_alert=True)

# ▶️ Botni ishga tushurish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
