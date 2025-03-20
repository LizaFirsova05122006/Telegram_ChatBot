from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3
from datetime import datetime


conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()


async def user_online_pay(callback: types.CallbackQuery, user_o):   # функция с заделкой на будущее (будет переделана при подключении платежной системы)
    #prices = [types.LabeledPrice(label="XTR", amount=0)]
    res = cursor.execute("SELECT id FROM orders WHERE id_telegram = ? AND cooked = ?", (callback.from_user.id, 1)).fetchall()
    free, name, sms, sumi, str_order = True, "", "", 0, ""
    if len(res) > 0 and len(res) % 2 == 0:
        builder = InlineKeyboardBuilder()
        builder.button(text="Оплатить ", callback_data="online_pay")
        for k, v in user_o.items():
            if v != 0:
                if free:
                    red = cursor.execute("SELECT price FROM drinks WHERE title = ?", (k,)).fetchall()
                    sumi += (v - 1) * red[0][0]
                    sms += k + " " + str(v) + "шт.\n"
                    str_order += k + " " + str(v) + "шт.\t"
                    free, name = False, k
                else:
                    red = cursor.execute("SELECT price FROM drinks WHERE title = ?", (k,)).fetchall()
                    sumi += v * red[0][0]
                    sms += k + " " + str(v) + "шт.\n"
                    str_order += k + " " + str(v) + "шт.\t"
        now = datetime.now()
        month, day, year = now.strftime("%m"), now.strftime("%d"), now.strftime("%Y")
        order = (callback.from_user.id, str_order, 0, 0, sumi, 0, "", 0, f"{day}.{month}.{year}")
        cursor.execute(
            "INSERT INTO orders (id_telegram, [order], cooked, pay, price, barista, num_order, preparing, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            order)
        conn.commit()
        await callback.message.answer(f"По нашей программе лояльности у Вас получилось {name} в подарок!\n"
                                      f"Заказ:\n{sms}\n"
                                      f"Сумма к оплате: {sumi}р.\n\n"
                                      f"Ваш заказ начнет готовиться, сразу после оплаты\n"
                                      f"Оплатите Ваш заказ\n", reply_markup=builder.as_markup())
        await callback.message.delete()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text="Оплатить ", callback_data="online_pay")
        for k, v in user_o.items():
            if v != 0:
                red = cursor.execute("SELECT price FROM drinks WHERE title = ?", (k,)).fetchall()
                sumi += v * red[0][0]
                sms += k + " " + str(v) + "шт.\n"
                str_order += k + " " + str(v) + "шт.\t"
        now = datetime.now()
        month, day, year = now.strftime("%m"), now.strftime("%d"), now.strftime("%Y")
        order = (callback.from_user.id, str_order, 0, 0, sumi, 0, "", 0, f"{day}.{month}.{year}")
        cursor.execute(
            "INSERT INTO orders (id_telegram, [order], cooked, pay, price, barista, num_order, preparing, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            order)
        conn.commit()
        await callback.message.answer(f"Заказ:\n{sms}\n"
                                      f"Сумма к оплате: {sumi}р.\n\n"
                                      f"Ваш заказ начнет готовиться, сразу после оплаты\n"
                                      f"Оплатите Ваш заказ\n", reply_markup=builder.as_markup())
        await callback.message.delete()
"""#await callback.message.answer_invoice(
       # chat_id=callback.message.chat.id,
       # title="Оплата заказа",
       # description="Оплатите заказ и мы начнем его готовить",
       # label='Заказ Онлайн в "Чашка Счастья"',
       # amount=30000
    #)"""


async def successful_pay(callback: types.CallbackQuery, user_order, bot: Bot):   # функция выдает номер заказа, будет изменена(или удалена), когда будет upgrate при подключении платежной системы
    res = cursor.execute("SELECT id FROM orders WHERE id_telegram = ?", (callback.from_user.id,)).fetchall()
    res1 = cursor.execute("SELECT id, id_telegram FROM barista").fetchall()
    min_i, max_i, sms = 0, len(res1), []
    now = datetime.now()
    month, day, year = now.strftime("%m"), now.strftime("%d"), now.strftime("%Y")
    number = str(day) + str(month) + str(year) + str(res[-1][0])
    cursor.execute("UPDATE orders SET pay = ?, barista = ?, num_order = ? WHERE id = ?", (1, res1[min_i][0], number, res[-1][0]))
    conn.commit()
    ing = [0, 0, 0, 0, 0]
    for k, v in user_order.items():
        if v > 0:
            sms.append(f"{k} - {v} шт.\n")
            if k == "Эспрессо":
                ing[0] += v * 9
            elif k == "Капучино":
                ing[0] += v * 9
                ing[1] += v * 120
            elif k == "Латте":
                ing[0] += v * 9
                ing[1] += v * 200
            elif k == "Флэт уайт":
                ing[0] += v * 18
                ing[1] += v * 120
            elif k == "Мокко":
                ing[0] += v * 9
                ing[1] += v * 150
                ing[2] += v * 20
            elif k == "Бамбл":
                ing[0] += v * 9
                ing[4] += v * 150
                ing[3] += v * 10
    await bot.send_message(chat_id=res1[min_i][1], text=f"❗УВЕДОМЛЕНИЕ ❗\n"
                                                        f"Новый заказ:\n"
                                                        f"{''.join(sms)}")
    await callback.message.answer(f"Заказ успешно оплачен. Мы начали его готовить\n"
                                  f"Ваш номер заказа: {number}")
    if min_i < max_i:
        min_i += 1
    else:
        min_i = 0
    for index, ingred in enumerate(ing):
        r = cursor.execute("SELECT expenditure FROM ingredients WHERE id = ?", (index + 1,)).fetchall()
        cursor.execute("UPDATE ingredients SET expenditure = ? WHERE id = ?", (r[0][0] + ingred, index + 1))
        conn.commit()