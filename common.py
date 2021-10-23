from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import keyboards as kb
import random as rm
from datebase import DateBase



async def rand_temp():
    a = 36.1
    b = 36.6
    temp = str(rm.uniform(a, b))[0:4]
    print(f"Температура {temp}, тип {type(temp)}")
    return temp

async def rand_press():
    syst_min = 120
    syst_max = 139
    diff_min = 35
    diff_max = 40

    syst_curr = rm.randint(syst_min, syst_max)
    diff_curr = rm.randint(diff_min, diff_max)
    dist_curr = syst_curr - diff_curr
    return str(syst_curr), str(dist_curr)



async def cmd_start(message: types.Message):
    await message.answer("Вас приветствует бот, предназначенный для контроля путевых листов. Для начала необходимо авторизоваться, для этого нажмине кнопку 'Регистрация'", reply_markup=kb.reg_menu)

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отмена", reply_markup=kb.menu)
    return



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    #dp.register_message_handler(cmd_cancel, Text(equals="Отменить", ignore_case=True), state="*")