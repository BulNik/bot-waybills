from aiogram import Dispatcher, types
from aiogram.types import BotCommand, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

but_reg = KeyboardButton("Регистрация")
but_start = KeyboardButton("Начало смены")
but_end = KeyboardButton("Закрыть смену")
but_status = KeyboardButton("Статус путевого листа")
but_cancel = KeyboardButton("Отменить")
but_delete = KeyboardButton("Удалить лист")
but_create = KeyboardButton("Создать путевой лист")
but_inspect = KeyboardButton("Пройти предрейсоввый осмотр")
probeg = KeyboardButton("Пробег")



reg_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_reg)
menu = ReplyKeyboardMarkup().add(but_start).add(but_end).add(but_status).add(but_cancel).add(but_delete)
sub_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_cancel)
sub_menu_org = ReplyKeyboardMarkup(resize_keyboard=True).add(but_create).add(but_cancel)
sub_menu_ip = ReplyKeyboardMarkup(resize_keyboard=True).add(but_inspect).add(but_cancel)
