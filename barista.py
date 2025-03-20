from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3
from aiogram import Bot
from datetime import datetime
from aiogram.types.input_file import FSInputFile


conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()


async def education(msg: types.Message):
    doc = FSInputFile(path="booklet.pdf")
    await msg.answer_document(doc, caption="Отправляю памятку по приготовлению кофе. Для удобства есть qr-коды с видеоуроками\n")


async def open_a_shift(msg: types.Message):
    res = cursor.execute("SELECT id from barista WHERE open = ? AND id_telegram = ?", (0, msg.from_user.id)).fetchall()
    now = datetime.now()
    h, m = now.strftime("%H"), now.strftime("%M")
    if len(res) != 0:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Открыть", callback_data="open"))
        await msg.answer(f"Откройте смену для того, чтобы принимать заказы\n", reply_markup=builder.as_markup())
    else:
        if int(h) >= 20 and int(m) >= 30:  # h >= 20 and m >= 30
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text="Закрыть", callback_data="close"))
            await msg.answer(f"Закройте смену и узнайте итоги дня\n", reply_markup=builder.as_markup())
        else:
            await msg.answer(f"День еще не закончился, Вы не можете закрыть смену!\n")


async def close_shift(callback: types.CallbackQuery):
    cursor.execute("UPDATE barista SET open = ? WHERE id_telegram = ?", (1, callback.from_user.id))
    conn.commit()
    res = cursor.execute("SELECT o.price FROM [orders] o JOIN barista b ON o.barista = b.id WHERE b.id_telegram = ? AND o.cooked = ?", (callback.from_user.id, 1)).fetchall()
    sumi = 0
    if len(res) > 0:
        sumi = sum(j for i in res for j in i)
    res1 = cursor.execute("SELECT id FROM barista WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    now = datetime.now()
    day, month, year = now.strftime("%d"), now.strftime("%m"), now.strftime("%Y")
    shif = (f"{day}.{month}.{year}", res1[0][0], sumi)
    cursor.execute("INSERT INTO shift (date, id_barista, revenue) VALUES (?, ?, ?)", shif)
    conn.commit()
    await callback.message.answer(f"Ваши итоги на {day}.{month}.{year}:\n"
                                  f"Количество выполненных заказов: {len(res)}\n"
                                  f"Выручка: {sumi}\n")


async def made_open(callback: types.CallbackQuery, bot: Bot):
    cursor.execute("UPDATE barista SET open = ? WHERE id_telegram = ?", (1, callback.from_user.id))
    conn.commit()
    await callback.message.answer(f"Смена успешно открыта\n")
    res = cursor.execute("SELECT id_telegram FROM queue").fetchall()
    if len(res) != 0:
        for i in res:
            await bot.send_message(chat_id=i[0], text=f"❗УВЕДОМЛЕНИЕ ❗\n"
                                                      f"Сотрудники открыли смену онлайн. Можете делать заказ\n")
        cursor.execute("DELETE FROM queue")
        conn.commit()


async def barista_orders(msg: types.Message):
    res = cursor.execute("SELECT o.id, o.[order], o.num_order price FROM [orders] o JOIN barista b ON o.barista = b.id WHERE b.id_telegram = ? AND o.cooked = ?", (msg.from_user.id, 0)).fetchall()
    if len(res) > 0:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Приготовить", callback_data="prepare"))
        await msg.answer(f"Всего заказов: {len(res)}\n\n"
                         f"Заказ № {res[0][2]}\n"
                         f"{'\n'.join(res[0][1].split('\t'))}", reply_markup=builder.as_markup())
    else:
        await msg.answer("Заказов пока нет!")


async def prepare(callback: types.CallbackQuery):
    res = cursor.execute("SELECT o.id FROM [orders] o JOIN barista b ON o.barista = b.id WHERE b.id_telegram = ?", (callback.from_user.id,)).fetchall()
    cursor.execute("UPDATE [orders] SET preparing = ? WHERE id = ?", (1, res[0][0]))
    conn.commit()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Готов к выдаче", callback_data="ready"))
    await callback.message.answer("Когда заказ будет готов, нажмите кнопку:", reply_markup=builder.as_markup())


async def ready_order(callback: types.CallbackQuery, bot: Bot):
    res = cursor.execute("SELECT o.id, o.price, o.num_order, o.barista, o.id_telegram FROM [orders] o JOIN barista b ON o.barista = b.id WHERE b.id_telegram = ? AND o.cooked = ?",(callback.from_user.id, 0)).fetchall()
    if not res:
        await bot.send_message(chat_id=callback.from_user.id, text="Нет непринятых заказов.")
        return
    cursor.execute("UPDATE [orders] SET cooked = ? WHERE num_order = ?", (1, res[0][2]))
    conn.commit()
    await bot.send_message(chat_id=res[0][4], text=f"❗️УВЕДОМЛЕНИЕ ❗️\n"
                                                   f"Ваш заказ № {res[0][2]} готов!")