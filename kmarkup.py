from aiogram import Bot, Dispatcher, executor, types

accept = types.InlineKeyboardMarkup(row_width=3)
accept.add(
    types.InlineKeyboardButton(text='✅ Принимаю', callback_data='accept')
)

apanel = types.InlineKeyboardMarkup(row_width=3)
apanel.add(
    types.InlineKeyboardButton(text='Статистика', callback_data='stats')
    )

accept = types.InlineKeyboardMarkup(row_width=3)
accept.add(
    types.InlineKeyboardButton(text='✅ Принимаю', callback_data='accept')
)

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
	types.KeyboardButton('👤 Баланс'),
	types.KeyboardButton('💸 Клик'),
	types.KeyboardButton('🎰 Вывод')
)
adminpanel = types.ReplyKeyboardMarkup(resize_keyboard=True)
adminpanel.add(
    types.KeyboardButton('Люди-Вывод')
)