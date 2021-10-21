import asyncio
import time
import datetime
import common
import logging
import random
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import keyboards as kb
from datebase import DateBase
from driver import Web

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
class States(StatesGroup):
    wait_check_id = State()
    wait_reg_name = State()
    wait_reg_ph_number = State()
    wait_start_check = State()
    wait_pr = State()



    wait_start_weybills = State()
    wait_end_weybills = State()
    wait_delete_waybill_befor = State()
    wait_delete_waybill_force = State()
    wait_check_ip = State()

    wait_start_ip = State()
    wait_start_org = State()






"""
    Проверки 
"""
async def check_id(user_id, user_name):
    logger.info(f"Функцию {check_id.__name__} вызвал {user_name} в {time.strftime('%X')}")
    sql = DateBase()
    print(user_id)
    res = await sql.select_item_where_id("users", "id", user_id)
    sql.db.close()
    if res is None:
        logger.info(f"Функция {check_id.__name__} завершена {user_name} в {time.strftime('%X')}")
        return None
    else:
        logger.info(f"Функция {check_id.__name__} завершена {user_name} в {time.strftime('%X')}")
        return True

async def check_name(name, user_name ):
    logger.info(f"Функцию {check_name.__name__} вызвал {user_name} в {time.strftime('%X')}")
    sql = DateBase()
    res = await sql.select_item_where_name("users", "name", name)
    sql.db.close()
    if res is None:
        logger.info(f"Функция {check_name.__name__} завершена {user_name} в {time.strftime('%X')}")
        return None
    else:
        logger.info(f"Функция {check_name.__name__} завершена {user_name} в {time.strftime('%X')}")
        return True

async def check_sub(user_id, user_name):
    logger.info(f"Функцию {check_sub.__name__} вызвал {user_name} в {time.strftime('%X')}")
    sql = DateBase()
    #res = await sql.select_item_where_id("users", "until", user_id)
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    now = datetime.datetime.strptime(now, '%d-%m-%Y')
    until = datetime.datetime.strptime(await sql.select_item_where_id("users", "until", user_id), '%d-%m-%Y')
    sql.db.close()

    if now < until:
        logger.info(f"Функция {check_sub.__name__} завершена {user_name} в {time.strftime('%X')}")
        return True
    else:
        logger.info(f"Функция {check_sub.__name__} завершена {user_name} в {time.strftime('%X')}")
        return False

async def check_status(user_id, user_name):
    logger.info(f"Функцию {check_status.__name__} вызвал {user_name} в {time.strftime('%X')}")
    sql = DateBase()
    res = await sql.select_item_where_id("users", "status", user_id)
    sql.db.close()
    if str(res) == "true":
        logger.info(f"Функция {check_status.__name__} завершена {user_name} в {time.strftime('%X')}")
        return True
    elif str(res) == "false":
        logger.info(f"Функция {check_status.__name__} завершена {user_name} в {time.strftime('%X')}")
        return False

async def check_time(user_id, user_name):
    logger.info(f"Функцию {check_time.__name__} вызвал {user_name} в {time.strftime('%X')}")
    logger.info("Проверка времени")
    stat = datetime.timedelta(hours=12)
    now_time = datetime.datetime.now()
    sql = DateBase()
    end_time = datetime.datetime.strptime(await sql.select_item_where_id("users", "end_at", user_id), '%Y-%m-%d %H:%M:%S.%f')
    logger.info(f"Время {end_time}")
    sql.db.close()
    delta = now_time - end_time
    if (delta > stat) == True:
        logger.info(f"{check_time.__name__} Прошло более 12 часов {user_name} в {time.strftime('%X')}")
        return True
    else:
        logger.info(f"{check_time.__name__} Прошло менее 12 часов {user_name} в {time.strftime('%X')}")
        return False

async def check_web_auth_park(web, user_name):
    if await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        logger.info(f"{check_web_auth_park.__name__} Удачная авторизация в ЛК Парка пользователя {user_name}")
        return True
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        logger.info(f"{check_web_auth_park.__name__} Не удалось авторизоваться в ЛК Парка пользователя {user_name}, неверное имя пользователя или пароль ")
        return False

async def check_web_auth_med(web, user_name):
    if await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        logger.info(f"{check_web_auth_med.__name__} Удачная авторизация в ЛК Медика {user_name}")
        return True
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        logger.info(f"{check_web_auth_med.__name__} Не удалось авторизоваться в ЛК Медика {user_name}, неверное имя пользователя или пароль ")
        return False

async def check_web_auth_mech(web, user_name):
    if await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        logger.info(f"{check_web_auth_mech.__name__} Удачная авторизация в ЛК Механика  {user_name}")
        return True
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        logger.info(f"{check_web_auth_mech.__name__} Не удалось авторизоваться в ЛК Механика  {user_name}, неверное имя пользователя или пароль ")
        return False

async def check_create_waybill(web, user_id, user_name):
    logger.info(f"Функцию {check_create_waybill.__name__} вызвал {user_name} в {time.strftime('%X')}")

    sql = DateBase()
    # Проверка создания путевого листа
    if await web.resource_check("MuiTypography-root MuiTypography-body1", "Создан путевой лист") == True:
        logger.info(f"Путевой лист пользователя {user_name} создан")
        sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{user_id}'")
        sql.db.commit()
        #await sql.update_item_by_id("users", "status", "false", user_id)
        #sql.db.close()
        return True
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Данные сохранены") == True:
        logger.info(f"Путевой лист пользователя {user_name} создан")
        sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{user_id}'")
        sql.db.commit()
        #await sql.update_item_by_id("users", "status", "false", user_id)
        #sql.db.close()
        return True
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Создан путевой лист") == False:
        logger.info(f"Неудалось создать путевой лист пользователя {user_name} ")
        web.browser.quit()
        sql.db.close()
        return False
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Данные сохранены") == False:
        logger.info(f"Неудалось создать путевой лист пользователя {user_name} ")
        web.browser.quit()
        sql.db.close()
        return False
    logger.info(f"Функция {check_create_waybill.__name__} завершена {user_name} в {time.strftime('%X')}")

async def check_aprove_med(web_med, user_id, user_name, done_time):
    logger.info(f"Функцию {check_aprove_med.__name__} вызвал {user_name} в {time.strftime('%X')}")

    if await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == True:
        logger.info(f"Путевой лист удачно одобрен медиком {user_name}")
        #sql = DateBase()
        #await sql.update_item_by_id("users", "id", done_time, user_id)
        #sql.db.close()
        return True
    elif await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == False:
        logger.info(f"Неудалось одобрить лист медиком {user_name}")
        web_med.browser.quit()
        return False
    logger.info(f"Функция {check_aprove_med.__name__} завершена {user_name} в {time.strftime('%X')}")

async def check_aprove_mech(web_mech, user_id, user_name, done_time):
    logger.info(f"Функцию {check_aprove_mech.__name__} вызвал {user_name} в {time.strftime('%X')}")
    if await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == True:
        logger.info(f"Путевой лист удачно одобрен механиком {user_name}")
        #sql = DateBase()
        #await sql.update_item_by_id("users", "id", done_time, user_id)
        #sql.db.close()
        return True
    elif await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == False:
        logger.info(f"Неудалось одобрить лист механиком {user_name}")
        web_mech.browser.quit()
        return False
    logger.info(f"Функция {check_aprove_mech.__name__} завершена {user_name} в {time.strftime('%X')}")


async def check_stat_waybill(message: types.Message, state: FSMContext):

    """
        Проверка на регистрацию
    """
    reg = await check_id(message.from_user.id, message.from_user.username)
    if reg == None:
        await message.answer("Вы не зарегистрированы", reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif reg == True:
        pass

    """
        Проверка на подписку
    """
    sub = await check_sub(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку", reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif sub == True:
        pass

    """
        Проверка на открытый путевой лист
    """
    status = await check_status(message.from_user.id, message.from_user.username)
    if status == False:
        await message.answer("Путевой лист открыт")
    elif status == True:
        await message.answer("Путевой лист закрыт")
    await state.finish()
    return


"""
    Регистрация пользователя 
"""
async def start_reg(message: types.Message, state: FSMContext):
    logger.info(f"Функцию {__name__} вызвал {message.from_user.username} в {time.strftime('%X')}")
    """
            Проверка на регистрацию
    """
    reg = await check_id(message.from_user.id, message.from_user.username)
    if reg == None:
        await message.answer("Вы не зарегистрированы", reply_markup=kb.reg_menu)
        await message.answer("Напишите ваше ФИО заглавными буквами (пример - Иванов Иван Иванович)", reply_markup=kb.sub_menu)
        await States.wait_reg_name.set()
        return
    elif reg == True:
        pass

    """
        Проверка на подписку
    """
    sub = await check_sub(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif sub == True:
        await message.answer(f"Успешная авторизация, добрый день {message.from_user.username}",reply_markup=kb.menu)
        await state.finish()




    logger.info(f"Функция {__name__} завершена {message.from_user.username} в {time.strftime('%X')}")

async def reg_name(message: types.Message, state: FSMContext):
    logger.info(f"Функцию {__name__} вызвал {message.from_user.username} в {time.strftime('%X')}")
    sql = DateBase()
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    logger.info(f"введено имя {user_data['name']}")
    res = await sql.select_item_where_name("users", "dogovor", user_data['name'])
    sql.db.close()
    if str(res) == "org":
        await message.answer("Напишите телефонный номер парка, начиная с 8", reply_markup=kb.sub_menu)
    elif str(res) == "ip":
        await message.answer("Напишите свой телефонный номер, зарегистрированный в КИС АРТ, начиная с 8", reply_markup=kb.sub_menu)
    await States.wait_reg_ph_number.set()
    logger.info(f"Функция {__name__} завершена {message.from_user.username} в {time.strftime('%X')}")

async def reg_number(message: types.Message, state: FSMContext):
    if len(message.text.lower()) != 11:
        await message.answer("Телефонный номер должен состоять из 11 символов")
        return
    logger.info(f"Функцию {__name__} вызвал {message.from_user.username} в {time.strftime('%X')}")
    await state.update_data(phone=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f"Ваше ФИО {user_data['name']}, номер телефона {user_data['phone']}", reply_markup=kb.sub_menu)
    sql = DateBase()
    res = await check_name(user_data['name'], message.from_user.username)
    if str(res) is None:
        await message.answer(f"Пользователь {user_data['name']} не зарегистрирован, обратитесь к администратору", reply_markup=kb.reg_menu)
        sql.db.close()
        await state.finish()
    else:
        await sql.update_item_by_name("users", "id", message.from_user.id, user_data['name'])
        await message.answer(f"Пользователь {user_data['name']} зарегистрирован", reply_markup=kb.menu)
        sql.db.close()
        await state.finish()
    logger.info(f"Функция {__name__} завершена {message.from_user.username} в {time.strftime('%X')}")

"""
    Работа с сайтом
"""
async def auth_park(user_id, user_name):
    url_login = 'https://art.taxi.mos.ru/login'
    sql = DateBase()
    phone_nubmer = await sql.select_item_where_id("users", "phone_number", user_id)
    password = await sql.select_item_where_id("users", "password", user_id)
    sql.db.close()
    web = Web()
    await web.get_page(url_login)
    await asyncio.sleep(5)
    await web.set_form_input("msisdn", phone_nubmer)
    await web.set_form_input_enter("password", password)
    await asyncio.sleep(5)
    auth = await check_web_auth_park(web, user_name)
    if auth == True:
        return True, web
    elif auth == False:
        web.browser.quit()
        return False, None

async def auth_med(user_name):
    url_login = 'https://art.taxi.mos.ru/login'
    med_login = "89257169519"
    med_passw = "1bRoSb1P"

    web_med = Web()
    await web_med.get_page(url_login)
    await web_med.set_form_input("msisdn", med_login)
    await web_med.set_form_input_enter("password", med_passw)
    await asyncio.sleep(5)
    auth = await check_web_auth_med(web_med, user_name)
    if auth == True:
        return True, web_med
    elif auth == False:
        web_med.browser.quit()
        return False, None

async def auth_mech(user_name):
    url_login = 'https://art.taxi.mos.ru/login'
    mech_login = "89773981068"
    mech_passw = "1HoEcX0Q"

    web_mech = Web()
    await web_mech.get_page(url_login)
    await web_mech.set_form_input("msisdn", mech_login)
    await web_mech.set_form_input_enter("password", mech_passw)
    await asyncio.sleep(5)
    auth = await check_web_auth_mech(web_mech, user_name)
    if auth == True:
        return True, web_mech
    elif auth == False:
        web_mech.browser.quit()
        return False, None

async def search_weybill_del(web, user_id):
    url_waybills = 'https://art.taxi.mos.ru/waybills'
    sql = DateBase()
    name = await sql.select_item_where_id("users", "name", user_id)
    print(name)
    sql.db.close()
    await web.get_page(url_waybills)
    await asyncio.sleep(5)
    await web.input_search(name.split(" ")[0])
    await asyncio.sleep(10)
    await web.choose_first()
    await web.click_button_only_text("span", "Удалить 1 запись")
    await web.click_button_only_text("span", "Oк")
    web.browser.quit()

async def create_waybill(web, user_id):
    url_waybills = 'https://art.taxi.mos.ru/waybills'
    sql = DateBase()
    name = await sql.select_item_where_id("users", "name", user_id)
    sql.db.close()
    await web.get_page(url_waybills)
    await web.click_button_with_text("span", "MuiButton-label", "Добавить")
    await web.wait_page_load()
    await web.set_form_input_enter_click("driver.id", name)
    await asyncio.sleep(10)
    await web.click_button_with_text("span", "MuiButton-label", "Сохранить")
    await web.wait_page_load()
    res = await check_create_waybill(web, user_id, name)
    if res == True:
        web.browser.quit()
        sql = DateBase()
        sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{user_id}'")
        sql.db.commit()
        #await sql.update_item_by_id("users", "status", "false", user_id)
        sql.db.close()
        return True
    elif res == False:
        web.browser.quit()
        return False

async def aprove_weybill_med(web_med, user_id, user_name):
    url_checkup  = "https://art.taxi.mos.ru/checkups"
    sql = DateBase()
    name = await sql.select_item_where_id("users", "name", user_id)
    sql.db.close()
    await web_med.get_page(url_checkup)
    await asyncio.sleep(5)
    await web_med.set_form_input_enter("publicId", name.split(" ")[0])
    await web_med.hover_click("MuiTableRow-root")
    # Одобрение путевого листа
    await web_med.svg_click()
    await web_med.set_form_input("checkupData.bodyTemperature", await common.rand_temp())
    syst_p, dist_p = await common.rand_press()
    await web_med.set_form_input("checkupData.bloodPressureSys", syst_p)
    await web_med.set_form_input("checkupData.bloodPressureDia", dist_p)
    await web_med.input_checkox("checkupData.alcoholTestPassed")
    await web_med.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    done_time = datetime.datetime.now().strftime('%H:%M %d.%m.%Y')
    aprove = await check_aprove_med(web_med, user_id, user_name, done_time)
    if aprove == True:
        web_med.browser.quit()
        return True, done_time
    elif aprove == False:
        return False, None

async def aprove_weybill_mech(web_mech, user_id, user_name, probeg):
    url_checkup  = "https://art.taxi.mos.ru/checkups"
    sql = DateBase()
    name = await sql.select_item_where_id("users", "name", user_id)
    sql.db.close()
    await web_mech.get_page(url_checkup)
    await asyncio.sleep(5)
    await web_mech.set_form_input_enter("publicId", name.split(" ")[0])
    await web_mech.hover_click("MuiTableRow-root")
    # Одобрение путевого листа
    await web_mech.svg_click()
    logger.info(f"Пробег {probeg}")
    await web_mech.set_form_input("checkupData.odometerData", probeg)
    await web_mech.input_checkox("checkupData.desinfected")
    await web_mech.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    done_time = datetime.datetime.now().strftime('%H:%M %d.%m.%Y ')
    done_time_db = datetime.datetime.now()
    aprove = await check_aprove_mech(web_mech, user_id, user_name, done_time)
    if aprove == True:
        web_mech.browser.quit()
        return True, done_time, done_time_db
    elif aprove == False:
        return False, None

async def close_waybill_med(web_med, user_id, user_name):
    url_checkup  = "https://art.taxi.mos.ru/checkups"
    await web_med.get_page(url_checkup)
    await asyncio.sleep(5)
    sql = DateBase()
    name = await sql.select_item_where_id("users", "name", user_id)
    sql.db.close()
    await web_med.set_form_input_enter("publicId", name.split(" ")[0])
    cl_1 = "MuiTableRow-root"
    await web_med.hover_click(cl_1)
    # Закрытие осмотра
    await web_med.svg_click()
    await web_med.input_checkox("checkupData.alcoholTestPassed")
    await web_med.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    data_time = datetime.datetime.now().strftime('%H:%M %d.%m.%Y')
    return data_time

async def close_waybill_mech(web_mech, user_id, user_name, probeg):
    url_checkup  = "https://art.taxi.mos.ru/checkups"
    await web_mech.get_page(url_checkup)
    await asyncio.sleep(5)
    sql = DateBase()
    name = await sql.select_item_where_id("users", "name", user_id)
    sql.db.close()
    await web_mech.set_form_input_enter("publicId", name.split(" ")[0])
    cl_1 = "MuiTableRow-root"
    await web_mech.hover_click(cl_1)

    # Закрытие осмотра
    await web_mech.svg_click()
    await web_mech.set_form_input("checkupData.odometerData", probeg)
    await web_mech.input_checkox("checkupData.washed")
    await web_mech.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    data_time = datetime.datetime.now().strftime('%H:%M %d.%m.%Y')
    data_end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    return data_time, data_end




"""
    Открытие путевого листа
"""
async def start_change_probeg(message: types.Message, state: FSMContext):
    logger.info(f"Функцию {__name__} вызвал {message.from_user.username} в {time.strftime('%X')}")

    """
            Проверка на регистрацию
    """
    reg = await check_id(message.from_user.id, message.from_user.username)
    if reg == None:
        await message.answer("Вы не зарегистрированы", reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif reg == True:
        pass

    """
        Проверка на подписку
    """
    sub = await check_sub(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif sub == True:
        pass

    """
        Проверка на открытую смену
    """
    sub = await check_status(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Путевой лист открыт, закройте смену, прежде чем открывать новую", reply_markup=kb.menu)
        await state.finish()
        return
    elif sub == True:
        pass

    await States.wait_start_check.set()
    await message.answer("Напишите ваш текущий пробег", reply_markup=kb.ReplyKeyboardRemove())
    logger.info(f"Функция {__name__} завершена {message.from_user.username} в {time.strftime('%X')}")

async def start_check(message: types.Message, state: FSMContext):
    await state.update_data(probeg=message.text.lower())
    user_data = await state.get_data()
    probeg = user_data['probeg']
    logger.info(f"Дебаг пробег {probeg}")
    sql = DateBase()
    dogovor = await sql.select_item_where_id("users", "dogovor", message.from_user.id)
    sql.db.close()
    if dogovor == "ip":
        await message.answer("Вы создали новый путевой лист в системе КИС АРТ?", reply_markup=kb.check_menu_ip)
        await States.wait_start_ip.set()
    elif dogovor == "org":
        # Проверка времени
        await message.answer("Проверка времени прошедшего с последней смены", reply_markup=kb.ReplyKeyboardRemove())
        time = await check_time(message.from_user.id, message.from_user.username)
        if time == True:
            await message.answer("C последней смены прошло более 12 часов")
            sql = DateBase()
            await sql.update_item_by_id("users", "probeg", probeg, message.from_user.id)
            sql.db.close()
            await message.answer("Подтвердите создание путевого листа", reply_markup=kb.sub_menu_org)
            await States.wait_start_org.set()
        elif time == False:
            await message.answer("C последней смены не прошло более 12 часов")
            await message.answer("Удаление предыдущего путевго листа. Ожидайте...", reply_markup=kb.ReplyKeyboardRemove())
            res, web = await auth_park(message.from_user.id, message.from_user.username)
            if res == False:
                await state.finish()
                await message.answer("Произошла ошибка при создании удалении путевого листа, повторите попытку через 1 минуту", reply_markup=kb.menu)
                return
            await asyncio.sleep(5)
            await search_weybill_del(web, message.from_user.id)
            await message.answer("Путевой лист удален")
            await asyncio.sleep(5)
            # обновить время
            cheat = datetime.timedelta(hours=13)
            sql = DateBase()
            end_time = datetime.datetime.strptime(await sql.select_item_where_id("users", "end_at", message.from_user.id),'%Y-%m-%d %H:%M:%S.%f')
            await sql.update_item_by_id("users", "end_at", end_time - cheat, message.from_user.id)
            sql.db.close()
            await message.answer("Подтвердите создание путевого листа. Ожидайте...", reply_markup=kb.sub_menu_org)
            await States.wait_start_org.set()

async def start_weybills_org(message: types.Message, state: FSMContext):
    try:
        await message.answer("Путевой лист в процессе создания", reply_markup=kb.ReplyKeyboardRemove())
        sql = DateBase()
        probeg = await sql.select_item_where_id("users", "probeg", message.from_user.id)
        sql.db.close()
        auth, web = await auth_park(message.from_user.id, message.from_user.username)
        if auth == False:
            await state.finish()
            await message.answer("Ошибка при создании путевого листа, повторите попытку через 1 минуту", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)

        post = await create_waybill(web, message.from_user.id)
        if post == True:
            await message.answer("Путевой лист создан")
            sql = DateBase()
            await sql.update_item_by_id("users", "status", "false", message.from_user.id)
            sql.db.close()
        elif post == False:
            await message.answer("Ошибка при создании путевого листа, повторите попытку через 1 минуту", reply_markup=kb.menu)
            await state.finish()
            return
        await asyncio.sleep(5)
        await message.answer("Прохождение предрейсового медосмотра")
        auth_md, web_med = await auth_med(message.from_user.username)
        if auth_md == False:
            await state.finish()
            await message.answer("Ошибка при прохождении медосмотра, обратитесь к администратору", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)
        aprove_md, done_time_md = await aprove_weybill_med(web_med, message.from_user.id, message.from_user.username)
        if aprove_md == True:
            await message.answer(f"Предрейсовый медосмотр пройден в {done_time_md}, мед. работник - Ворфоломеева О.А.")
        elif aprove_md == False:
            await message.answer("Ошибка при прохождении медосмотра, обратитесь к администратору", reply_markup=kb.menu)
            await state.finish()
            return
        logger.info("Типа задержка")
        await asyncio.sleep(1)
        #await asyncio.sleep(random.randint(240, 420))
        await message.answer("Прохождение предрейсового техосмотра")
        auth_mh, web_mech = await auth_mech(message.from_user.username)
        if auth_mh == False:
            await state.finish()
            await message.answer("Ошибка при прохождении техосмотра, обратитесь к администратору", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)
        aprove_mh, done_time_mh, done_time_db = await aprove_weybill_mech(web_mech, message.from_user.id, message.from_user.username, probeg)
        if aprove_mh == True:
            await message.answer(f"Предрейсовый техосмотр пройден в {done_time_mh}, механик - Соколов Е.А. Выезд разрешен", reply_markup=kb.menu)
        elif aprove_mh == False:
            await message.answer("Ошибка при прохождении техосмотра, обратитесь к администратору", reply_markup=kb.menu)
            await state.finish()
            return
        sql = DateBase()
        await sql.update_item_by_id("users", "start_at", done_time_db, message.from_user.id)
        sql.db.close()

        # Очистка ресурсов
        try:
            web_med.browser.quit()
            web_mech.browser.quit()
            web.browser.quit()
            sql.db.close()
        except:
            pass
        finally:
            await state.finish()
    except Exception as ex:
        logger.info(f" {start_weybills_org.__name__}: Произошла ошибка {ex}")
        await message.answer("Произошла ошибка во время начала смены, обратитесь к администратору")
        await state.finish()
        return

async def start_weybills_ip(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() != "да":
            await message.answer("Прежде всего необходимо создать новый путевой лист", reply_markup=kb.menu)
            await state.finish()
            return
        sql = DateBase()
        await sql.update_item_by_id("users", "status", "false", message.from_user.id)
        sql.db.close()
        await message.answer("Прохождение предрейсового медосмотра", reply_markup=kb.ReplyKeyboardRemove())
        sql = DateBase()
        probeg = await sql.select_item_where_id("users", "probeg", message.from_user.id)
        sql.db.close()
        auth_md, web_med = await auth_med(message.from_user.username)
        if auth_md == False:
            await state.finish()
            await message.answer("Ошибка при прохождении медосмотра, обратитесь к администратору", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)
        aprove_md, done_time_md = await aprove_weybill_med(web_med, message.from_user.id, message.from_user.username)
        if aprove_md == True:
            await message.answer(f"Предрейсовый медосмотр пройден в {done_time_md}, мед. работник - Ворфоломеева О.А.")
        elif aprove_md == False:
            await message.answer("Ошибка при прохождении медосмотра, обратитесь к администратору", reply_markup=kb.menu)
            await state.finish()
            return
        logger.info("Типа задерэка ")
        await asyncio.sleep(1)
        #await asyncio.sleep(random.randint(240, 420))
        await message.answer("Прохождение предрейсового техосмотра")
        auth_mh, web_mech = await auth_mech(message.from_user.username)
        if auth_mh == False:
            await state.finish()
            await message.answer("Ошибка при прохождении техосмотра, обратитесь к администратору", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)
        aprove_mh, done_time_mh, done_time_db = await aprove_weybill_mech(web_mech, message.from_user.id,
                                                                          message.from_user.username, probeg)
        if aprove_mh == True:
            await message.answer(f"Предрейсовый техосмотр пройден в {done_time_mh}, механик - Соколов Е.А. Выезд разрешен",
                                 reply_markup=kb.menu)
        elif aprove_mh == False:
            await message.answer("Ошибка при прохождении техосмотра, обратитесь к администратору", reply_markup=kb.menu)
            await state.finish()
            return
        sql = DateBase()
        await sql.update_item_by_id("users", "start_at", done_time_db, message.from_user.id)
        sql.db.close()

        # Очистка ресурсов
        try:
            web_med.browser.quit()
            web_mech.browser.quit()
            sql.db.close()
        except:
            pass
        finally:
            await state.finish()
    except Exception as ex:
        logger.info(f" {start_weybills_org.__name__}: Произошла ошибка {ex}")
        sql = DateBase()
        await sql.update_item_by_id("users", "status", "true", message.from_user.id)
        sql.db.close()
        await message.answer("Произошла ошибка во время начала смены, создайте новый путевой лист или обратитесь к администратору", reply_markup=kb.menu)
        await state.finish()
        return

"""
    Закрытие путевого листа
"""
async def end_change_probeg(message: types.Message, state: FSMContext):
    logger.info(f"Функцию {__name__} вызвал {message.from_user.username} в {time.strftime('%X')}")

    """
            Проверка на регистрацию
    """
    reg = await check_id(message.from_user.id, message.from_user.username)
    if reg == None:
        await message.answer("Вы не зарегистрированы", reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif reg == True:
        pass

    """
        Проверка на подписку
    """
    sub = await check_sub(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif sub == True:
        pass

    """
       Проверка на открытую смену
    """
    sub = await check_status(message.from_user.id, message.from_user.username)
    if sub == True:
        await message.answer("Смена закрыта", reply_markup=kb.menu)
        await state.finish()
        return
    elif sub == False:
        pass

    await States.wait_end_weybills.set()
    await message.answer("Напишите ваш текущий пробег", reply_markup=kb.ReplyKeyboardRemove())
    logger.info(f"Функция {__name__} завершена {message.from_user.username} в {time.strftime('%X')}")

async def end_weybills(message: types.Message, state: FSMContext):
    try:
        await state.update_data(probeg=message.text.lower())
        user_data = await state.get_data()
        probeg = user_data['probeg']
        sql = DateBase()
        await sql.update_item_by_id("users", "probeg", probeg, message.from_user.id)
        sql.db.close()
        await message.answer(f"Пробег обновлен", reply_markup=kb.ReplyKeyboardRemove())

        await message.answer("Прохождение послерейсового медосмотра")
        auth_md, web_med = await auth_med(message.from_user.username)
        if auth_md == False:
            await state.finish()
            await message.answer("Ошибка при прохождении медосмотра, обратитесь к администратору", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)
        data_time = await close_waybill_med(web_med, message.from_user.id, message.from_user.username)
        await message.answer(f"Послерейсовый медосмотр пройден в {data_time}, мед. работник - Ворфоломеева О.А.")
        logger.info("Типа задержка")
        await asyncio.sleep(1)
        # await asyncio.sleep(random.randint(240, 420))
        await message.answer("Прохождение послерейсового техосмотра")
        auth_mh, web_mech = await auth_mech(message.from_user.username)
        if auth_mh == False:
            await state.finish()
            await message.answer("Ошибка при прохождении техосмотра, обратитесь к администратору", reply_markup=kb.menu)
            return
        await asyncio.sleep(5)
        data_time, data_end = await close_waybill_mech(web_mech, message.from_user.id, message.from_user.username, probeg)
        await message.answer(f"Послерейсовый техосмотр пройден в {data_time}, механик - Соколов Е.А.")
        await message.answer("Смена закрыта", reply_markup=kb.menu)
        sql = DateBase()
        await sql.update_item_by_id("users", "status", 'true', message.from_user.id)
        await sql.update_item_by_id("users", "end_at", data_end, message.from_user.id)
        sql.db.close()

        # Очистка ресурсов
        try:
            web_med.browser.quit()
            web_mech.browser.quit()
            sql.db.close()
        except:
            pass
        finally:
            await state.finish()
    except Exception as ex:
        logger.info(f" {start_weybills_org.__name__}: Произошла ошибка {ex}")
        await message.answer("Произошла ошибка во время закрытия смены, обратитесь к администратору")
        await state.finish()
        return

"""
    Удаление путевых листов
"""
# Удаление листа если 12 часов не прошло
async def delete_weybills_befor(message: types.Message, state: FSMContext):
    await message.answer("Удаление предыдущего путевго листа", reply_markup=kb.sub_menu)
    res, web = await auth_park(message.from_user.id, message.from_user.username)
    if res == False:
        await state.finish()
        await message.answer("Произошла ошибка при создании удалении путевого листа, повторите попытку через 1 минуту")
        return
    await asyncio.sleep(5)
    await search_weybill_del(web, message.from_user.id)
    await message.answer("Путевой лист удален")
    await asyncio.sleep(5)
    # обновить время
    cheat = datetime.timedelta(hours=13)
    sql = DateBase()
    end_time = datetime.datetime.strptime(await sql.select_item_where_id("users", "end_at", message.from_user.id), '%Y-%m-%d %H:%M:%S.%f')
    await sql.update_item_by_id("users", "end_at", end_time - cheat, message.from_user.id)
    dogovor = await sql.select_item_where_id("users", "dogovor", message.from_user.id)
    sql.db.close()
    # переход состояния
    if dogovor == "org":
        await message.answer("Подтвердите создание путевого листа", reply_markup=kb.sub_menu_org)
        await States.wait_start_org.set()
    elif dogovor == "ip":
        await message.answer("Подтвердите прохождение предрейсового осмотра", reply_markup=kb.sub_menu_ip)
        await States.wait_start_ip.set()

# Удаление листа ручное
async def delete_weybills_force(message: types.Message, state: FSMContext):
    logger.info(f"Функцию {__name__} вызвал {message.from_user.username} в {time.strftime('%X')}")

    """
            Проверка на регистрацию
    """
    reg = await check_id(message.from_user.id, message.from_user.username)
    if reg == None:
        await message.answer("Вы не зарегистрированы", reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif reg == True:
        pass

    """
        Проверка на подписку
    """
    sub = await check_sub(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif sub == True:
        pass

    """
        Проверка на открытую смену
    """
    sub = await check_status(message.from_user.id, message.from_user.username)
    if sub == True:
        await message.answer("Путевой лист закрыт", reply_markup=kb.menu)
        await state.finish()
        return
    elif sub == False:
        pass


    await message.answer("Удаление предыдущего путевго листа. Ожидайте...", reply_markup=kb.sub_menu)
    res, web = await auth_park(message.from_user.id, message.from_user.username)
    if res == False:
        await state.finish()
        await message.answer("Произошла ошибка при создании удалении путевого листа, повторите попытку через 1 минуту")
        return
    await asyncio.sleep(5)
    await search_weybill_del(web, message.from_user.id)
    await message.answer("Путевой лист удален", reply_markup=kb.menu)
    await asyncio.sleep(5)
    # обновить время
    cheat = datetime.timedelta(hours=13)
    sql = DateBase()
    end_time = datetime.datetime.strptime(await sql.select_item_where_id("users", "end_at", message.from_user.id),
                                          '%Y-%m-%d %H:%M:%S.%f')
    print(end_time - cheat)
    """
           Откатить время окончания смены если удаляется закрытий лист, в ином случае изменить только статус 
    """
    sub = await check_status(message.from_user.id, message.from_user.username)
    if sub == True:
        await sql.update_item_by_id("users", "end_at", end_time - cheat, message.from_user.id)
        logger.info("Изменено время окончания")
    elif sub == False:
        await sql.update_item_by_id("users", "status", 'true', message.from_user.id)
        logger.info("Изменен статус листа")

    #await sql.update_item_by_id("users", "end_at", end_time - cheat, message.from_user.id)
    #await sql.update_item_by_id("users", "status", 'true', message.from_user.id)
    sql.db.close()

async def cmd_cancel(message: types.Message, state: FSMContext):

    """
                Проверка на регистрацию
        """
    reg = await check_id(message.from_user.id, message.from_user.username)
    if reg == None:
        await message.answer("Вы не зарегистрированы", reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif reg == True:
        pass

    """
        Проверка на подписку
    """
    sub = await check_sub(message.from_user.id, message.from_user.username)
    if sub == False:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        await state.finish()
        return
    elif sub == True:
        pass

    await state.finish()
    await message.answer("Отмена", reply_markup=kb.menu)
    return

async def pr(message: types.Message, state: FSMContext):
    await message.answer("Пробег")
    await States.wait_pr.set()

async def change_pr(message: types.Message, state: FSMContext):
    sql = DateBase()
    #await state.update_data(pr=message.text.lower())
    #user_data = await state.get_data()
    #pr = user_data['pr']
    done_time_db = datetime.datetime.now()
    #sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{message.from_user.id}'")
    #sql.db.commit()
    print(done_time_db)

    await sql.update_item_by_id("users", "start_at", done_time_db, message.from_user.id)

    #await sql.update_item_by_id_test("users", "probeg", pr, message.from_user.id)


def register_handlers_choose(dp: Dispatcher):


    dp.register_message_handler(start_reg, Text(equals="Регистрация", ignore_case=True), state="*")
    dp.register_message_handler(reg_name, state=States.wait_reg_name)
    dp.register_message_handler(reg_number, state=States.wait_reg_ph_number)

    dp.register_message_handler(start_change_probeg, Text(equals="Начало смены", ignore_case=True), state="*")
    dp.register_message_handler(start_check, state=States.wait_start_check)
    dp.register_message_handler(start_weybills_ip, state=States.wait_start_ip)
    dp.register_message_handler(start_weybills_org, state=States.wait_start_org)

    dp.register_message_handler(delete_weybills_befor, state=States.wait_delete_waybill_befor)
    dp.register_message_handler(delete_weybills_force, Text(equals="Удалить лист", ignore_case=True), state="*")

    dp.register_message_handler(check_stat_waybill, Text(equals="Статус путевого листа", ignore_case=True), state="*")

    dp.register_message_handler(end_change_probeg, Text(equals="Закрыть смену", ignore_case=True), state="*")
    dp.register_message_handler(end_weybills, state=States.wait_end_weybills)

    dp.register_message_handler(cmd_cancel, Text(equals="Отменить", ignore_case=True), state="*")

    dp.register_message_handler(pr, Text(equals="Пробег", ignore_case=True), state="*")
    dp.register_message_handler(change_pr, state=States.wait_pr)











