from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = "8053741398:AAEXeDe7vVRMA3FDNI4vaBimQUC47DENSxM"  # Bot tokeningizni yozing

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Homiy kanallar
CHANNELS = {
    "HOMIY kanalimiz ": "@kompyuter_telegram_chanel",
    "HOMIY guruximiz ": "@AqlliUyinchoqlar"
}

# Obuna tekshirish
async def check_subscription(user_id):
    not_subscribed = []
    for name, channel in CHANNELS.items():
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append((name, channel))
        except Exception:
            not_subscribed.append((name, channel))
    return not_subscribed


# Start komandasi
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    not_subscribed = await check_subscription(message.from_user.id)

    if not not_subscribed:
        await message.answer("✅ Xush kelibsiz! Endi botdan foydalanishingiz mumkin. Emoji, gif va stecker yuboring😊🤝")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for name, link in not_subscribed:
            keyboard.add(InlineKeyboardButton(text=f"📢 {name}", url=f"https://t.me/{link.replace('@', '')}"))
        keyboard.add(InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs"))

        await message.answer(
            "🤖 Botdan foydalanish uchun quyidagi homiy kanallarga obuna bo‘ling!:",
            reply_markup=keyboard
        )


# Tekshirish tugmasi
@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def check_subs_handler(callback_query: types.CallbackQuery):
    not_subscribed = await check_subscription(callback_query.from_user.id)

    if not not_subscribed:
        await callback_query.message.edit_text("✅ Xush kelibsiz! Endi botdan foydalanishingiz mumkin. emoji, stecker va gif yuboring, men sizga id ma'lumot beraman😊🤝")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for name, link in not_subscribed:
            keyboard.add(InlineKeyboardButton(text=f"📢 {name}", url=f"https://t.me/{link.replace('@', '')}"))
        keyboard.add(InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs"))

        await callback_query.message.edit_text(
            "⚠️ Siz hali hamma homiy kanallarga obuna bo‘lmadingiz!\n"
            "Iltimos, avval obuna bo‘ling:",
            reply_markup=keyboard
        )


# Emoji, Sticker, Rasm, GIF ID chiqarish
@dp.message_handler(content_types=["text", "sticker", "photo", "animation"])
async def id_handler(message: types.Message):
    # Emoji yoki matn belgilarini ko‘rsatish
    if message.text:
        response = []
        for ch in message.text:
            if not ch.isalnum() and not ch.isspace():
                response.append(f"{ch} → U+{ord(ch):X}")
        if response:
            await message.answer("🔢 Emoji / Belgi ID lari:\n" + "\n".join(response))

    # Sticker bo‘lsa
    if message.sticker:
        text = (
            f"🖼 Sticker ma’lumotlari:\n\n"
            f"📌 file_id:\n<code>{message.sticker.file_id}</code>\n\n"
            f"📌 file_unique_id:\n<code>{message.sticker.file_unique_id}</code>\n\n"
        )
        if message.sticker.emoji:
            text += f"😃 Emoji: {message.sticker.emoji} → U+{ord(message.sticker.emoji):X}"
        await message.answer(text, parse_mode="HTML")

    # Rasm bo‘lsa (eng katta sifatli file_id ni olamiz)
    if message.photo:
        photo = message.photo[-1]  # eng katta rasm
        await message.answer(
            f"🖼 Rasm file_id:\n<code>{photo.file_id}</code>",
            parse_mode="HTML"
        )

    # GIF (animation) bo‘lsa
    if message.animation:
        text = (
            f"🎞 GIF ma’lumotlari:\n\n"
            f"📌 file_id:\n<code>{message.animation.file_id}</code>\n\n"
            f"📌 file_unique_id:\n<code>{message.animation.file_unique_id}</code>"
        )
        await message.answer(text, parse_mode="HTML")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
