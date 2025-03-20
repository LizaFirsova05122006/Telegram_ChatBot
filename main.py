import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from web import keep_alive
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import sqlite3
import asyncio
from admin import user_messages, regular_messages, awaiting_response, make_a_schedule, inventory_accounting, menu_a
from users import made_order, order_selection, send_answer_no, menu, loyalty_program, view_the_history_order#, return_q
from barista import open_a_shift, made_open, barista_orders, prepare, ready_order, close_shift, education
from month import jan, feb, mar, apr, mayy, jun, jul, aug, sep, oct, nov, dec
from system_notifications import send_answer_yes
from payment import user_online_pay, successful_pay
from aiogram.utils.keyboard import InlineKeyboardBuilder


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()
waiting_num, waiting_answers, id_answer, waiting_count = False, False, 0, False
waiting_text = False
coffe_int = False
drinks = ["Эспрессо", "Капучино", "Латте", "Флэт уайт", "Мокко", "Бамбл"]
order_pay = {"Эспрессо": 0, "Капучино": 0, "Латте": 0, "Флэт уайт": 0, "Мокко": 0, "Бамбл": 0}
user_order = []
queue = []
schedule = True


@dp.message(Command('start'))
async def command_start(msg: types.Message):
    if msg.from_user.is_bot:   # проверка написал смс бот
        await msg.answer(f'Здравствуйте!👋 Я бот кофейни "Чашка Счастья".\n'
                         f'Извините, но мы не отвечаем ботам.\n'
                         f'Если у Вас есть вопросы или нужна помощь, пожалуйста, напишите мне как человек! 😊')
    else:
        res = cursor.execute("SELECT role_id FROM people WHERE telegram_id = ?", (msg.from_user.id,)).fetchall()
        if len(res) > 0 and res[0][0] == 1:   # администратор
            kb = [
                [types.KeyboardButton(text="Учет запасов")],
                [types.KeyboardButton(text="Меню")],
                [types.KeyboardButton(text="Сообщения пользователей")]
            ]
            m_start = (f'Приветствую, администратор {msg.chat.first_name}!👋\n'
                       f'На данный момент возможно:\n'
                       f'~ "Учет запасов" - не стоит беспокоится я напомню, когда пора будет заказывать ингредиенты\n'
                       f'~ "Меню" - можно посмотреть меню\n'
                       f'~ "Сообщения пользователей" - обратная связь от посетителей\n')
        elif len(res) > 0 and res[0][0] == 2:   # бариста
            kb = [
                [types.KeyboardButton(text="Заказы")],
                [types.KeyboardButton(text="Обучение")],
                [types.KeyboardButton(text="Калькулятор")],
                [types.KeyboardButton(text="Смена")]
            ]
            m_start = (f'Приветствую, бариста {msg.chat.first_name}!👋\n'
                       f'На данный момент возможно:\n'
                       f'~ "Заказы" - посмотреть очередь заказов\n'
                       f'~ "Обучение" - получить информацию и советы по приготовлению кофе\n'
                       f'~ "Калькулятор" - расчитать вес кофе в чашке\n'
                       f'~ "Смена" - открыть и закрыть смену, получить информацию за день\n')
        else:   # пользователь
            kb = [
                [types.KeyboardButton(text="Сделать заказ")],
                [types.KeyboardButton(text="Меню")],
                [types.KeyboardButton(text="Программа лояльности")],
                [types.KeyboardButton(text="Обратная связь")],
                [types.KeyboardButton(text="Посмотреть историю заказов")]
            ]
            m_start = (f'Приветствую, {msg.chat.first_name}!👋\n'
                       f'Я бот кофейни "Чашка Счастья". Вот что я могу:\n'
                       f'~ "Сделать заказ" - сделайте заказ онлайн и не стойте в очереди\n'
                       f'~ "Меню" - все любимые позиции в одном месте\n'
                       f'~ "Программа лояльности" - для постоянных клиентов\n'
                       f'~ "Обратная связь" - нам очень важно Ваше мнение\n'
                       f'~ "Посмотреть историю заказов" - проверьте свои предыдушие заказы\n')
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        res1 = cursor.execute("SELECT name FROM people WHERE telegram_id = ?", (msg.chat.id,)).fetchall()
        if len(res1) == 0:
            user = (msg.chat.id, 3, msg.chat.first_name)
            cursor.execute("INSERT INTO people (telegram_id, role_id, name) VALUES (?, ?, ?)", user)
            conn.commit()
        await msg.answer(m_start, reply_markup=keyboard)


@dp.message(F.text.lower() == "калькулятор")  # бариста
async def calculator(msg: types.Message):
    global coffe_int
    coffe_int = True
    await msg.answer("Введите вес молотого кофе в грамм:")


@dp.message(F.text.lower() == "учет запасов")  # администратор
async def inventory_a(msg: types.Message):
    await inventory_accounting(msg)


@dp.message(F.text.lower() == "обучение")   # бариста
async def educat(msg: types.Message):
    await education(msg)


@dp.message(F.text.lower() == "посмотреть историю заказов")   # пользователь
async def view_tho(msg: types.Message):
    await view_the_history_order(msg)


@dp.message(F.text.lower() == "программа лояльности")   # пользователь
async def loyalty_p(msg: types.Message):
    await loyalty_program(msg)


@dp.message(F.text.lower() == "заказы")   # бариста
async def barista_o(msg: types.Message):
    await barista_orders(msg)


@dp.message(F.text.lower() == "смена")   # бариста
async def open_shift(msg: types.Message):
    await open_a_shift(msg)


@dp.callback_query(F.data == "January")   # месяцы
async def January(callback: types.CallbackQuery):
    await jan(callback)


@dp.callback_query(F.data == "February")
async def February(callback: types.CallbackQuery):
    await feb(callback)


@dp.callback_query(F.data == "March")
async def March(callback: types.CallbackQuery):
    await mar(callback)


@dp.callback_query(F.data == "April")
async def April(callback: types.CallbackQuery):
    await apr(callback)


@dp.callback_query(F.data == "May")
async def May(callback: types.CallbackQuery):
    await mayy(callback)


@dp.callback_query(F.data == "June")
async def June(callback: types.CallbackQuery):
    await jun(callback)


@dp.callback_query(F.data == "July")
async def July(callback: types.CallbackQuery):
    await jul(callback)


@dp.callback_query(F.data == "August")
async def August(callback: types.CallbackQuery):
    await aug(callback)


@dp.callback_query(F.data == "September")
async def September(callback: types.CallbackQuery):
    await sep(callback)


@dp.callback_query(F.data == "October")
async def October(callback: types.CallbackQuery):
    await oct(callback)


@dp.callback_query(F.data == "November")
async def November(callback: types.CallbackQuery):
    await nov(callback)


@dp.callback_query(F.data == "December")
async def December(callback: types.CallbackQuery):
    await dec(callback)


@dp.callback_query(F.data == "close")   # бариста
async def close_s(callback: types.CallbackQuery):
    await close_shift(callback)


@dp.callback_query(F.data == "yes")   # система
async def send_a_y(callback: types.CallbackQuery):
    await send_answer_yes(callback, bot)


@dp.callback_query(F.data == "no")   # пользователь
async def send_a_n(callback: types.CallbackQuery):
    await send_answer_no(callback)


@dp.callback_query(F.data == "open")   # бариста
async def opening(callback: types.CallbackQuery):
    await made_open(callback, bot)


@dp.message(F.text.lower() == "сообщения пользователей")   # администратор
async def user_m(msg: types.Message):
    await user_messages(msg)


@dp.callback_query(F.data == "prepare")   # бариста
async def preparing(callback: types.CallbackQuery):
    await prepare(callback)


@dp.callback_query(F.data == "ready")   # бариста
async def ready_o(callback: types.CallbackQuery):
    await ready_order(callback, bot)


@dp.callback_query(F.data == "no_admin")   # администратор
async def regular_m(callback: types.CallbackQuery):
    await regular_messages(callback)


@dp.callback_query(F.data == "admin")   # администратор
async def awaiting_r(callback: types.CallbackQuery):
    await awaiting_response(callback)


@dp.callback_query(F.data == "yes_a")   # администратор
async def admin_answer(callback: types.CallbackQuery):
    global waiting_num
    waiting_num = True
    await callback.message.answer(f"Пришлите № сообщения, на который хотели бы ответить\n")


@dp.message(F.text.lower() == "сделать заказ")   # пользователь
async def made_orders(msg: types.Message):
    await made_order(msg)


@dp.callback_query(F.data == "order")  # пользователь
async def made(callback: types.CallbackQuery):
    await order_selection(callback)


@dp.callback_query(F.data == "espresso")
async def espresso(callback: types.CallbackQuery):
    global user_order, waiting_count
    user_order.append(["Эспрессо"])
    waiting_count = True
    await callback.message.answer(f"Ваш выбор: Эспрессо\n"
                                  f"Укажите количество (написать необходимо одно число)\n")
    await callback.message.delete()


@dp.callback_query(F.data == "cappuccino")
async def cappuccino(callback: types.CallbackQuery):
    global user_order, waiting_count
    user_order.append(["Капучино"])
    waiting_count = True
    await callback.message.answer(f"Ваш выбор: Капучино\n"
                                  f"Укажите количество (написать необходимо одно число)\n")
    await callback.message.delete()


@dp.callback_query(F.data == "latte")
async def latte(callback: types.CallbackQuery):
    global user_order, waiting_count
    user_order.append(["Латте"])
    waiting_count = True
    await callback.message.answer(f"Ваш выбор: Латте\n"
                                  f"Укажите количество (написать необходимо число)\n")
    await callback.message.delete()


@dp.callback_query(F.data == "flat_white")
async def flat_white(callback: types.CallbackQuery):
    global user_order, waiting_count
    user_order.append(["Флэт уайт"])
    waiting_count = True
    await callback.message.answer(f"Ваш выбор: Флэт уайт\n"
                                  f"Укажите количество (написать необходимо число)\n")
    await callback.message.delete()


@dp.callback_query(F.data == "mokko")
async def mokko(callback: types.CallbackQuery):
    global user_order, waiting_count
    user_order.append(["Мокко"])
    waiting_count = True
    await callback.message.answer(f"Ваш выбор: Мокко\n"
                                  f"Укажите количество (написать необходимо число)\n")
    await callback.message.delete()


@dp.callback_query(F.data == "bumble")
async def bumble(callback: types.CallbackQuery):
    global user_order, waiting_count
    user_order.append(["Бамбл"])
    waiting_count = True
    await callback.message.answer(f"Ваш выбор: Бамбл\n"
                                  f"Укажите количество (написать необходимо число)\n")
    await callback.message.delete()


@dp.callback_query(F.data == "no_order")   # оплата
async def do_not_order(callback: types.CallbackQuery):
    global order_pay
    await user_online_pay(callback, order_pay)


@dp.callback_query(F.data == "online_pay")  # оплата прошла, и пользователю отдается номер заказа
async def online_p(callback: types.CallbackQuery):
    global order_pay
    await successful_pay(callback, order_pay, bot)
    order_pay = {"Эспрессо": 0, "Капучино": 0, "Латте": 0, "Флэт уайт": 0, "Мокко": 0, "Бамбл": 0}


@dp.pre_checkout_query()   # проверка, что оплата запрошена
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)   # если успешно прошла оплата
async def procces_successful(msg: types.Message):
    await msg.answer(f'{msg.successful_payment.telegram_payment_charge_id}',
                     message_effect_id="5104841245755180586")


@dp.callback_query(F.data == "yes_order")  # пользователь
async def do_yes_order(callback: types.CallbackQuery):
    await order_selection(callback)


@dp.message(F.text.lower() == "обратная связь")   # пользователь
async def feedback(msg: types.Message):
    global waiting_text
    waiting_text = True
    await msg.answer(f"Напишите, пожалуйста, Ваше сообщение\n")


@dp.message(F.text.lower() == "меню")   # пользователь
async def send_menu(msg: types.Message):
    res = cursor.execute("SELECT role_id FROM people WHERE telegram_id = ?", (msg.from_user.id,)).fetchall()
    if res[0][0] == 1:
        await menu_a(msg)
    else:
        await menu(msg)


@dp.message()
async def messages(msg: types.Message):
    global waiting_num, waiting_answers, id_answer, waiting_count, user_order, waiting_text, order_pay, coffe_int
    res = cursor.execute("SELECT role_id FROM people WHERE telegram_id = ?", (msg.from_user.id,)).fetchall()
    if waiting_num and res[0][0] == 1:
        if msg.text.isdigit():
            res3 = cursor.execute("SELECT text_answer FROM question WHERE id = ?", (msg.text, )).fetchall()
            await msg.answer(f"Напишите Ваше сообщение для пользователя\n"
                             f"Напомню сообщение пользователя:\n"
                             f"{res3[0][0]}")
            waiting_num, waiting_answers, id_answer = False, True, int(msg.text)
        else:
            await msg.answer(f"Пришлите № сообщения, на который хотели бы ответить\n")
    elif coffe_int and res[0][0] == 2:
        if msg.text.isdigit():
            c = (20 / 100) * int(msg.text) / (10 / 100)
            await msg.answer(f"Вес кофе в чашке: {c:.2f} грамм")
            coffe_int = False
        else:
            await msg.answer("Пришлите, пожалуйста, вес молотого кофе в грамм одним числом!")
    elif waiting_answers and res[0][0] == 1:
        res4 = cursor.execute("SELECT telegram_id FROM question WHERE id = ?", (id_answer, )).fetchall()
        try:
            await bot.send_message(chat_id=res4[0][0], text=f"❗Уведомление❗\n"
                                                            f"Ответ от администратора\n"
                                                            f"{msg.text}\n")
            cursor.execute("UPDATE question SET answer = ? WHERE id = ?", (1, id_answer))
            conn.commit()
        except Exception:
            await msg.answer("Не получилось отправить сообщение попробуйте позднее\n")
        id_answer, waiting_answers = 0, False
    elif waiting_count and res[0][0] == 3:
        if msg.text.isdigit():
            if order_pay[user_order[-1][0]] <= 5:
                if int(msg.text) <= 5 and order_pay[user_order[-1][0]] + int(msg.text) <= 5:
                    user_order[-1].append(int(msg.text))
                    order_pay[user_order[-1][0]] += int(msg.text)
                    waiting_count, builder = False, InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(text="Да", callback_data="yes_order"))
                    builder.add(types.InlineKeyboardButton(text="Нет", callback_data="no_order"))
                    await msg.answer(f"Хотели бы добавить к заказу что-то еще?\n", reply_markup=builder.as_markup())
                else:
                    await msg.answer(f"Для одного напитка у нас действуют ограничения: не более 5шт.\n"
                                     f"Вы можете добавить: {5 - order_pay[user_order[-1][0]]}шт.\n"
                                     f"Укажите, пожалуйста, количество для {user_order[-1][0]} (одно число)\n")
            else:
                await msg.answer(f"Для одного напитка у нас действуют ограничения: не более 5шт.\n")
                waiting_count = False
        else:
            await msg.answer(f"Укажите, пожалуйста, количество для {user_order[-1][0]} (одно число)\n")
    elif waiting_text and res[0][0] == 3:
        answer = (msg.text, msg.chat.id, 0, 0)
        cursor.execute("INSERT INTO question (text_answer, telegram_id, ans_admin, answer) VALUES (?, ?, ?, ?)", answer)
        conn.commit()
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Да", callback_data="yes"))
        builder.add(types.InlineKeyboardButton(text="Нет", callback_data="no"))
        await msg.answer("Требуется ли ответ администратора на Ваше сообщение?", reply_markup=builder.as_markup())
        waiting_text = False


async def main():
    await dp.start_polling(bot)

keep_alive()
if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())