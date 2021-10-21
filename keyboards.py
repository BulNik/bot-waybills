from aiogram import Dispatcher, types
from aiogram.types import BotCommand, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

but_reg = KeyboardButton("Регистрация")
but_start = KeyboardButton("Начало смены")
but_end = KeyboardButton("Закрыть смену")
but_status = KeyboardButton("Статус путевого листа")
but_cancel = KeyboardButton("Отменить")
#but_delete = KeyboardButton("Удалить лист")
but_create = KeyboardButton("Создать путевой лист")
but_inspect = KeyboardButton("Пройти предрейсовый осмотр")
probeg = KeyboardButton("Пробег")
but_y = KeyboardButton("Да")
but_n = KeyboardButton("Нет")




reg_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_reg)
menu = ReplyKeyboardMarkup().add(but_start).add(but_end).add(but_status)
sub_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_cancel)
sub_menu_org = ReplyKeyboardMarkup(resize_keyboard=True).add(but_create).add(but_cancel)
sub_menu_ip = ReplyKeyboardMarkup(resize_keyboard=True).add(but_inspect).add(but_cancel)
check_menu_ip = ReplyKeyboardMarkup(resize_keyboard=True).add(but_y).add(but_n).add(but_cancel)
