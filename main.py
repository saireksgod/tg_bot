import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import text as tx
import kmarkup as k
import Function as fc

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = sqlite3.connect('data.db')
sql = db.cursor()

@dp.message_handler(commands=['start', 'help'])  # Начало работы
async def start(message: types.Message):
    sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
    result = sql.fetchall()
    if len(result) == 0:
        sql.execute(f"INSERT INTO users (user_id, balance, name)"
                  f"VALUES ('{message.chat.id}', '0', '{message.from_user.mention}')")
        db.commit()
        await message.answer(tx.sogl, parse_mode='Markdown', reply_markup=k.accept)
    else:
        await message.answer(
            f'Здарово, {message.from_user.mention}, кликай и зарабатывай голду бесплатно!\n За каждый клик вам начисляется 50 копеек на баланс.', reply_markup=k.menu)


@dp.message_handler(content_types=["text"])  # Реакция на текст
async def reaction(message: types.Message):
    chat_id = message.chat.id
    fc.first(chat_id=chat_id)
    if message.text == '👤 Баланс':
        bal = sql.execute(f'SELECT balance FROM users WHERE user_id = "{message.chat.id}"').fetchone()
        db.commit()
        await message.answer(f'Ваш баланс: {fc.toFixed(bal[0], 1)}')

    elif message.text == '💸 Клик':
        sql.execute(f'UPDATE users SET balance = balance + 0.5 WHERE user_id IS "{message.chat.id}"')
        db.commit()

        await message.answer('Вам начислено +0.5')

    elif message.text == '🎰 Вывод':
        ballan = sql.execute(f'SELECT balance FROM users WHERE user_id = "{message.chat.id}"').fetchone()
        vivo = sql.execute(f'SELECT vivod FROM users WHERE user_id = "{message.chat.id}"').fetchone()
        db.commit()
        if ballan[0] <= 150:
            await message.answer(tx.ver)
        elif vivo[0] == 1:
            await message.answer(f"Заявка на вывод была уже отправлена, ожидайте пока с вами свяжутся")
        else:
            sql.execute(f'UPDATE users SET vivod = 1 WHERE user_id IS "{message.chat.id}"')
            await message.answer(f'Заявка на вывод успешно отправлена администраторам, с вами скоро свяжутся.', reply_markup=k.menu)
            await bot.send_message(admin, f'Новая заявка на вывод:\nID - {message.chat.id}\nЮзернейм - {message.from_user.mention}\n[Ссылка на пользователя]({message.from_user.url})\nБаланс - {fc.toFixed(ballan[0], 1)}\nСвяжитесь с пользователем, чтобы отправить ему деньги.', parse_mode='Markdown')
            #await bot.send_message(admin2, f'Новая заявка на вывод:\nID - {message.chat.id}\nЮзернейм - {message.from_user.mention}\n[Ссылка на пользователя]({message.from_user.url})\nБаланс - {fc.toFixed(ballan[0], 1)}\nСвяжитесь с пользователем, чтобы отправить ему деньги.',parse_mode='Markdown')
    # elif message.text == '🎰 Вывод':
    #     payed = q.execute(f'SELECT payd FROM users WHERE user_id = "{message.chat.id}"').fetchone()
    #     connection.commit()
    #     if payed[0] == 0:
    #         await message.answer(tx.ver, reply_markup=k.pay)
    #     else:
    #         bal = q.execute(f'SELECT balance FROM users WHERE user_id = "{message.chat.id}"').fetchone()
    #         connection.commit()
    #         await message.answer(f'Заявка на вывод успешно отправлена администраторам, с вами скоро свяжутся.',
    #                              reply_markup=k.menu)
    #         await bot.send_message(admin,
    #                                f'Новая заявка на вывод:\nID - {message.chat.id}\nЮзернейм - {message.from_user.mention}\n[Ссылка на пользователя]({message.from_user.url})\nБаланс - {fc.toFixed(bal[0], 1)}\nСвяжитесь с пользователем, чтобы отправить ему деньги.',
    #                                parse_mode='Markdown')
    #         q.execute(f"UPDATE USERS SET payd = 0 WHERE user_id = {chat_id}")
    #         connection.commit()
    # elif message.text == 'Оплатить':
    #     link = fc.pay(chat_id=chat_id)
    #     await message.answer(f'Ваш ID - {message.chat.id}\nК оплате - {sum}₽\n[Ссылка для оплаты]({link})',
    #                          reply_markup=k.buy1, parse_mode='Markdown')

    elif message.text == '/admin':
        if str(chat_id) == str(admin):
            await message.answer('Добро пожаловать в админ панель:', reply_markup=k.apanel)
        else:
            pass
            # await message.answer('Черт! Ты меня взломал🙃')
    elif message.text == '/apanel':
        if str(chat_id) == str(admin):
            await  bot.send_message(admin, f'Вы вошли в режим администратора!', reply_markup=k.adminpanel)
        else:
            pass
    elif message.text == 'Люди-Вывод':
        if str(chat_id) == str(admin):
            wer = sql.execute(f'SELECT * FROM users WHERE vivod = 1').fetchall()
            viv = len(wer)
            await message.answer(f'{viv}')

@dp.callback_query_handler(lambda call: True)  # Inline часть
async def cal(call):
    chat_id = call.message.chat.id
    if call.data == 'stats':
        re = sql.execute(f'SELECT * FROM users').fetchall()
        kol = len(re)
        bal = sql.execute(f"SELECT sum(balance) FROM users").fetchone()
        db.commit()
        await call.message.answer(
            f'Всего пользователей: {kol}\nОбщий баланс всех пользователей: {fc.toFixed(bal[0], 1)}')
    elif call.data == 'back':
        await call.message.answer('Назад..', reply_markup=k.menu)
    elif call.data == 'accept':
        await call.message.answer(
            f'Привет, {call.from_user.mention}, кликай и зарабатывай! За каждый клик вам начисляется 50 копеек на баланс.',
            reply_markup=k.menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Запуск
