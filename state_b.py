from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# Значения вопросов
menu_1 =       ["Путевой лист", "Пробег", "Профиль", "Статус"]
level =           ["бак", "маг"]
subject_IT_B  = ["Мат", "Рус"]
subject_IT_M  = ["Фил", "Инф"]
subject_SIS_B = ["Анг", "Нем"]
subject_SIS_M = ["Физ", "Сет"]
subject_RIT_B = ["Кан", "Пер"]
subject_RIT_M = ["Вок", "Вло"]

class States(StatesGroup):
    wait_reg_name = State()
    wait_reg_ph_number = State()


# Ответ на команду /choose и первый вопрос
async def reg_start(message: types.Message):

    '''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавляем все значения факультетов на клавиатуру
    for fac in menu_1:
        keyboard.add(fac)
    # ожидаем ответа на вопрос
    '''
    await message.answer("Напишите ваше ФИО")
    # Встать в состояние
    await States.wait_reg_name.set()


# Выбор вакультета
async def reg_name(message: types.Message, state: FSMContext):
    '''
    if message.text.lower() not in faculty:
        await message.answer("Пожалуйста, выберите факультет, используя клавиатуру ниже.")
        return
    '''
    # Сохранение значения состояния ключ: значение
    await state.update_data(chosen_fac=message.text.lower())
    '''
    # Вывод на клавиатуру уровни проф подготовки
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lvl in level:
        keyboard.add(lvl)
    '''
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await States.next()
    await message.answer("Теперь выберите уровень профессиональной подготовки:", reply_markup=keyboard)

# Выбор уровня подготовки
async def lvl_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in level:
        await message.answer("Пожалуйста, выберите уровень подготовки, используя клавиатуру ниже.")
        return

    user_data = await state.get_data()
    await message.answer(f"Ваш факультет {message.text.lower()}, уровень подготовки {user_data['chosen_fac']}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_choose(dp: Dispatcher):
    dp.register_message_handler(choose_start, commands="choose", state="*")
    dp.register_message_handler(fac_chosen, state=States.waiting_for_faculty_name)
    dp.register_message_handler(lvl_chosen, state=States.waiting_for_level)