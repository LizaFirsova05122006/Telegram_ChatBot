from aiogram import types
import sqlite3
from aiogram import Bot


conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()


async def send_answer_yes(callback: types.CallbackQuery, bot: Bot):   # функция отправки админу системного уведомления, что пришло сообщение от пользователя
    res1 = cursor.execute("SELECT id, text_answer FROM question WHERE telegram_id = ?",
                          (callback.from_user.id,)).fetchall()
    cursor.execute("UPDATE question SET ans_admin = ? WHERE id = ?", (1, res1[-1][0]))
    conn.commit()
    await callback.message.answer(f"Ваше мнение важно для нас. 🤗\n"
                                  "В течении 7 дней с Вами свяжется администратор.\n"
                                  "Напоминаю, что администратор имеет право не ответить в "
                                  "случае, если посчитает сообщение некорректным\n")
    try:
        await bot.send_message(chat_id=1881303315, text=f"❗УВЕДОМЛЕНИЕ ❗\n"
                                                        f"Новое сообщение от пользователя\n")
    except Exception:
        await callback.message.answer("Произошли неполадки и я не смог отправить "
                                      "Ваше сообщение. Но не переживайте, "
                                      "администратор обязательно увидит Ваше сообщение\n")