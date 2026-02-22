import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ❗ Tokenni bu yerga yozing (BotFather’dan olgan YANGI token)
BOT_TOKEN = "8527964792:AAHis0i7ZfnpINBExROMf46JFxzcBw9UEs8"

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

# Xizmatlar ro'yxati (xohlasangiz o'zgartiring)
SERVICES = [
    ("Hayoti", "svc:Hayoti"),
    ("Oilasi", "svc:Oilasi"),
    ("O‘qish joyi", "svc:Oqish"),
    ("Yutuqlari", "svc:Yutuqlari"),
     ("bog'lanish", "svc:Boglanish"),
]

def services_keyboard():
    kb = InlineKeyboardBuilder()
    for text, data in SERVICES:
        kb.button(text=text, callback_data=data)
    kb.adjust(2)  # 2 tadan qatorda
    return kb.as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! ✅\n\n"
        "Quyidagi Toshtemirov Mirshoxidning ma'lumotlaridan birini tanlang:",
        reply_markup=services_keyboard()
    )

@dp.callback_query(F.data.startswith("svc:"))
async def service_chosen(call: CallbackQuery):
    service = call.data.split(":", 1)[1]
    await call.answer()

    if service == "Hayoti":
        text = """
👤 Mirshoxid Toshtemirov

2004-yilda tug‘ilgan.
Faol, o‘z ustida ishlaydigan va yangi texnologiyalarga qiziqadigan inson.

Doimo rivojlanish, o‘rganish va kelajakda katta maqsadlarga erishishni niyat qilgan.
"""

    elif service == "Oilasi":
        text = """
👨‍👩‍👦 Oilasi haqida

Mirshoxid Toshtemirov mehribon va qo‘llab-quvvatlovchi oilada ulg‘aygan.

Oila uning hayotida eng muhim qadriyatlardan biri hisoblanadi.
"""

    elif service == "Oqish":
        text = """
🎓 O‘qish joyi

Mirshoxid Toshtemirov hozirda bilim olish va o‘zini rivojlantirish bilan shug‘ullanmoqda.

Zamonaviy texnologiyalar, IT sohasi va yangi bilimlarni o‘rganishga katta qiziqish bildiradi.
"""

    elif service == "Yutuqlari":
        text = """
🏆 Yutuqlari

✔ O‘z ustida doimiy ishlaydi  
✔ Yangi ko‘nikmalarni tez o‘zlashtiradi  
✔ Texnologiya va dasturlashga qiziqadi  
✔ Kelajak uchun aniq maqsadlari bor
"""
    elif service == "Boglanish":
        text = """
📞 Bog‘lanish
✔ Tel: +998 94 004 70 19
✔ Tg:@kouichi_m  
✔ Email: mirshoxidtoshtemirov04@gmail.com 
"""

    else:
        text = "Ma’lumot topilmadi."

    await call.message.answer(text)
# ✅ Mini App tg.sendData(...) yuborgan narsani ushlab oladi (sizdagi eski funksiya)
@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    raw = message.web_app_data.data  # JSON string
    try:
        data = json.loads(raw)
    except Exception:
        await message.answer(f"📦 WebAppData keldi (JSON emas):\n{raw}")
        return

    if data.get("type") == "survey":
        service = data.get("service")
        note = (data.get("note") or "").strip()
        counter = data.get("counter")

        u = data.get("user") or {}
        uname = u.get("username")
        full_name = ((u.get("first_name") or "") + " " + (u.get("last_name") or "")).strip()
        who = f"@{uname}" if uname else (full_name or "Foydalanuvchi")

        text = (
            "✅ So‘rov qabul qilindi!\n\n"
            f"👤 Kim: {who}\n"
            f"🧩 Xizmat: {service}\n"
            f"🔢 Counter: {counter}\n"
        )
        if note:
            text += f"\n📝 Izoh: {note}"

        await message.answer(text)
    else:
        await message.answer(f"📦 Data keldi:\n{data}")

async def main():
    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())