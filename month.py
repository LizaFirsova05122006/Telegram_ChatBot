from aiogram import types
import sqlite3
from aiogram.enums import ParseMode


conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()


async def jan(callback: types.CallbackQuery):   # январь
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Январь:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 1:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 1:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def feb(callback: types.CallbackQuery):   # февраль
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Февраль:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 2:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 2:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def mar(callback: types.CallbackQuery):   # март
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Март:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 3:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 3:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def apr(callback: types.CallbackQuery):   # апрель
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Апрель:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 4:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 4:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def mayy(callback: types.CallbackQuery):   # май
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Май:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 5:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 5:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def jun(callback: types.CallbackQuery):   # июнь
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Июнь:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 6:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 6:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def jul(callback: types.CallbackQuery):   # июль
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Июль:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 7:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 7:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def aug(callback: types.CallbackQuery):   # август
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Август:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 8:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 8:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def sep(callback: types.CallbackQuery):   # сентябрь
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Сентябрь:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 9:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 9:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def oct(callback: types.CallbackQuery):   # октябрь
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Октябрь:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 10:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 10:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def nov(callback: types.CallbackQuery):   # ноябрь
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Ноябрь:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 11:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 11:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)


async def dec(callback: types.CallbackQuery):   # декабрь
    res = cursor.execute("SELECT date, [order] FROM [orders] WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    year_db = set(int(list(i)[0].split(".")[2]) for i in res)
    sms = "<b>Ваши заказы за Декабрь:</b>\n"
    for i, d in enumerate(year_db):
        if len(year_db) > 1:
            sms += f"<b>{str(i + 1)}</b>" + f"<b>)</b> " + f"<b>{str(d)}:</b>" + "\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 12:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
        else:
            sms += f"<b>{str(d)}:</b>\n"
            for j in range(len(res)):
                if int(res[j][0].split(".")[1]) == 12:
                    sms += f"<b>Дата:</b>" + res[j][0] + f"\n<b>Заказ:</b>\n" + "\n".join(res[j][1].split("\t"))
    await callback.message.answer(sms, parse_mode=ParseMode.HTML)