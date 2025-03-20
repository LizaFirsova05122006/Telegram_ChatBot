from aiogram import types
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3
import asyncio
from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder

conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()


async def menu_a(msg: types.Message):
    photos = MediaGroupBuilder()
    photos.add_photo(FSInputFile("img/menu/1.jpg"))
    await msg.answer_media_group(media=photos.build())


async def inventory_accounting(msg: types.Message):
    res = cursor.execute("SELECT title, expenditure, reserve FROM ingredients").fetchall()
    sms, req = "", "\n❗<b>Рекомендации:</b>❗\n"
    for i in res:
        sms += f"<b>{i[0]}</b>\nИзрасховадано: {i[1]} {'гр.' if i[0] == 'Кофе' else 'мл.'}\nОсталось: {i[2] - i[1]} {'гр.' if i[0] == 'Кофе' else 'мл.'}\n"
        if i[0] == "Кофе" and i[2] - i[1] < 150:
            req += "Заказать кофе\n"
        elif i[0] == "Молоко" and i[2] - i[1] < 600:
            req += "Заказать молоко\n"
        elif i[0] == "Шоколадный сироп" and i[2] - i[1] < 300:
            req += "Заказать шоколадный сироп\n"
        elif i[0] == "Карамельный сироп" and i[2] - i[1] < 300:
            req += "Заказать карамельный сироп\n"
        elif i[0] == "Апельсиновый сок" and i[2] - i[1] < 300:
            req += "Заказать апельсиновый сок\n"
    if len(req) > 24:
        sms += req
    await msg.answer(sms, parse_mode=ParseMode.HTML)


async def user_messages(msg: types.Message):   # функция реакция на смс "сообщения пользователей"
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Ожидающие ответа", callback_data="admin"))
    builder.add(types.InlineKeyboardButton(text="Обычные", callback_data="no_admin"))
    await msg.answer("Какие сообщения показать?", reply_markup=builder.as_markup())


async def regular_messages(callback: types.CallbackQuery):   # функция реакция на инлайн-кнопку "Обычные"
    res = cursor.execute("SELECT text_answer, telegram_id, id FROM question WHERE ans_admin = ?", (0,)).fetchall()
    await callback.message.answer(f"Ожидайте, выгружаю данные...⏳\n")
    await asyncio.sleep(1)
    for i in res:
        await callback.message.answer(f"Сообщение № {i[2]}\n"
                                      f"От пользователя с id = {i[1]}\n"
                                      f"Текст сообщения:\n"
                                      f"{i[0]}\n")
        await asyncio.sleep(1)
    await callback.message.answer(f"Все сообщения успешно выгружены!\n")


async def awaiting_response(callback: types.CallbackQuery):   # функция реакция на инлайн-кнопку "Ожидающие ответа"
    res1 = cursor.execute("SELECT text_answer, telegram_id, id FROM question WHERE ans_admin = ?", (1,)).fetchall()
    await callback.message.answer(f"Ожидайте, выгружаю данные...⏳\n")
    await asyncio.sleep(1)
    for i in res1:
        await callback.message.answer(f"Сообщение № {i[2]}\n"
                                      f"От пользователя с id = {i[1]}\n"
                                      f"Текст сообщения:\n"
                                      f"{i[0]}\n")
        await asyncio.sleep(1)
    build = InlineKeyboardBuilder()
    build.add(types.InlineKeyboardButton(text="Да", callback_data="yes_a"))
    await callback.message.answer(f"Желаете ли ответить на какое-нибудь сообщение?\n", reply_markup=build.as_markup())


async def make_a_schedule(msg: types.Message):
    await msg.answer(f"Отправь мне файл\n")