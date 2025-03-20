from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
import asyncio
import sqlite3


PHOTOS_FOLDER = "img/menu/"
conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()


async def view_the_history_order(msg: types.Message):
    month = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь", 7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
    month_e = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    res = cursor.execute("SELECT date FROM [orders] WHERE id_telegram = ?", (msg.from_user.id,)).fetchall()
    if len(res) > 0:
        builder = InlineKeyboardBuilder()
        sms = "Я могу показать историю за:\n"
        month_db = set(int(j.split(".")[1]) for i in res for j in list(i))
        for g in month_db:
            builder.button(text=str(g), callback_data=month_e[g])
            sms += f"<b>{str(g)})</b>" + " " + f"<b>{month[g]}</b>" + "\n"
        await msg.answer(sms, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
    else:
        await msg.answer("Вы еще не делали заказов в нашей кофейне!\nСамое время начать!")


async def loyalty_program(msg: types.Message):
    res = cursor.execute("SELECT id FROM [orders] WHERE id_telegram = ? AND cooked = ?", (msg.from_user.id, 1)).fetchall()
    county = len(res)
    if county % 11 == 0:
        await msg.answer(f"В следующем заказе для Вас один напиток будет бесплатный!")
    else:
        await msg.answer(f"В нашей кофейне действует акция: каждый 12 заказ один напиток в подарок!\n"
                         f"До бесплатного напитка Вам осталось: {12 - res[0][0]}\n")


async def made_order(msg: types.Message):
    f_date = msg.date
    h, m = f_date.strftime("%H"), f_date.strftime("%M")
    if (int(h) + 3) < 9:
        await msg.answer(f"Извините, но наша кофейня еще не открылась. "
                         f"Напоминаем, что часы работы с 9:00 до 21:00 по МСК. "
                         f"Заказы принимаем до 20:30 по МСК")
    elif (int(h) + 3) >= 20 and int(m) > 30:  # h >= 20
        await msg.answer(f"Извините, но мы не успеем приготовить Ваш кофе. "
                         f"Напоминаем, что часы работы с 9:00 до 21:00 по МСК. "
                         f"Заказы принимаем до 20:30 по МСК.")
    else:
        res0 = cursor.execute("SELECT id FROM barista WHERE open = ?", (1, )).fetchall()
        if len(res0) == 0:
            await msg.answer(f"Извините, но сотрудники еще не открыли онлайн-смену. мы сообщим Вам, как только это станет возможным\n")
            res1 = cursor.execute("SELECT id FROM queue WHERE id_telegram = ?", (msg.from_user.id,)).fetchall()
            if len(res1) == 0:
                cursor.execute("INSERT INTO queue (id_telegram) VALUES (?)", (msg.from_user.id, ))
                conn.commit()
        else:
            res = cursor.execute("SELECT id FROM ingredients WHERE title = ? AND expenditure <= ?",
                                 ("Кофе", 482)).fetchall()
            if len(res) == 0:
                await msg.answer(f"Извините, мы не сможем приготовить Ваш напиток. У нас не хватает ингредиентов.\n")
            else:
                photos = MediaGroupBuilder()
                photos.add_photo(FSInputFile("img/menu/1.jpg"))
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(text="Сделать заказ", callback_data="order"))
                await msg.answer_media_group(media=photos.build())
                await asyncio.sleep(1)
                await msg.answer(f"Готовы сделать заказ?", reply_markup=builder.as_markup())


async def order_selection(callback: types.CallbackQuery):   # функция реакция на инлайн-кнопку "Сделать заказ" или "Да", чтобы добавить что-то к заказу
    builder = InlineKeyboardBuilder()
    milk = cursor.execute("SELECT id FROM ingredients WHERE title = ? AND expenditure <= ?", ("Молоко", 400)).fetchall()
    if len(milk) == 0:  # молока не хватает мы можем приготовить что-то кроме эспрессо
        builder.add(types.InlineKeyboardButton(text="Эспрессо", callback_data="espresso"))
        await callback.message.answer(f"Я могу предложить для заказа только Эспрессо\n", reply_markup=builder.as_markup())
    else:  # молока для всех хватит
        choco = cursor.execute("SELECT id FROM ingredients WHERE title = ? AND expenditure <= ?", ("Шоколадный сироп", 940)).fetchall()
        caramel = cursor.execute("SELECT id FROM ingredients WHERE title = ? AND expenditure <= ?", ("Карамельный сироп", 960)).fetchall()
        sok = cursor.execute("SELECT id FROM ingredients WHERE title = ? AND expenditure <= ?", ("Апельсиновый сок", 700)).fetchall()
        if len(choco) == 0 and len(caramel) > 0 and len(sok) > 0:  # нельзя приготовить мокко
            builder.add(types.InlineKeyboardButton(text="1", callback_data="espresso"))
            builder.add(types.InlineKeyboardButton(text="2", callback_data="cappuccino"))
            builder.add(types.InlineKeyboardButton(text="3", callback_data="latte"))
            builder.add(types.InlineKeyboardButton(text="4", callback_data="flat_white"))
            builder.add(types.InlineKeyboardButton(text="5", callback_data="bumble"))
            message = (f"Чтобы оформить заказ, пожалуйста, выбирите позиции ниже и нажмите ниже:\n"
                       f"1. Эспрессо\n"
                       f"2. Капучино\n"
                       f"3. Латте\n"
                       f"4. Флэт уайт\n"
                       f"5. Бамбл\n")
        elif len(choco) > 0 and (len(caramel) == 0 or len(sok) == 0): # не можем приготовить бамбл
            builder.add(types.InlineKeyboardButton(text="1", callback_data="espresso"))
            builder.add(types.InlineKeyboardButton(text="2", callback_data="cappuccino"))
            builder.add(types.InlineKeyboardButton(text="3", callback_data="latte"))
            builder.add(types.InlineKeyboardButton(text="4", callback_data="flat_white"))
            builder.add(types.InlineKeyboardButton(text="5", callback_data="mokko"))
            message = (f"Чтобы оформить заказ, пожалуйста, выбирите позиции ниже и нажмите ниже:\n"
                       f"1. Эспрессо\n"
                       f"2. Капучино\n"
                       f"3. Латте\n"
                       f"4. Флэт уайт\n"
                       f"5. Мокко\n")
        elif len(choco) == 0 and len(caramel) == 0 and len(sok) == 0: # и не мокко и не бамбл
            builder.add(types.InlineKeyboardButton(text="1", callback_data="espresso"))
            builder.add(types.InlineKeyboardButton(text="2", callback_data="cappuccino"))
            builder.add(types.InlineKeyboardButton(text="3", callback_data="latte"))
            builder.add(types.InlineKeyboardButton(text="4", callback_data="flat_white"))
            message = (f"Чтобы оформить заказ, пожалуйста, выбирите позиции ниже и нажмите ниже:\n"
                       f"1. Эспрессо\n"
                       f"2. Капучино\n"
                       f"3. Латте\n"
                       f"4. Флэт уайт\n")
        else:
            builder.add(types.InlineKeyboardButton(text="1", callback_data="espresso"))
            builder.add(types.InlineKeyboardButton(text="2", callback_data="cappuccino"))
            builder.add(types.InlineKeyboardButton(text="3", callback_data="latte"))
            builder.add(types.InlineKeyboardButton(text="4", callback_data="flat_white"))
            builder.add(types.InlineKeyboardButton(text="5", callback_data="mokko"))
            builder.add(types.InlineKeyboardButton(text="6", callback_data="bumble"))
            message = (f"Чтобы оформить заказ, пожалуйста, выбирите позиции ниже и нажмите ниже:\n"
                       f"1. Эспрессо\n"
                       f"2. Капучино\n"
                       f"3. Латте\n"
                       f"4. Флэт уайт\n"
                       f"5. Мокко\n"
                       f"6. Бамбл\n")
        await callback.message.answer(message, reply_markup=builder.as_markup())


async def send_answer_no(callback: types.CallbackQuery):   # функция отправки пользователю сообщения, если ответ не требует ответа администратора
    await callback.message.answer(f"Ваше мнение важно для нас. 🤗\n"
                                  f"Спасибо!\n")


async def menu(msg: types.Message):
    photos = MediaGroupBuilder()
    photos.add_photo(FSInputFile("img/menu/1.jpg"))
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Сделать заказ", callback_data="order"))
    await msg.answer_media_group(media=photos.build())
    await asyncio.sleep(1)
    await msg.answer(f"Желаете сделать заказ?\n", reply_markup=builder.as_markup())