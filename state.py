import time
import datetime
import common
import random
import os
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import keyboards as kb
from datebase import DateBase
from driver import Web

class States(StatesGroup):
    wait_check_id = State()
    wait_reg_name = State()
    wait_reg_ph_number = State()
    wait_start_weybills = State()
    wait_end_weybills = State()
    wait_delete_waybills = State()
    wait_start_ip = State()
    wait_start_org = State()



async def check_id(message: types.Message, state: FSMContext):
    sql = DateBase()
    sql.cur.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if sql.cur.fetchone() is None:
        await message.answer(f"Вы не авторизованы")
        await message.answer("Напишите ваше ФИО заглавными буквами", reply_markup=kb.sub_menu)
        await States.wait_reg_name.set()
    else:
        now = datetime.datetime.now().strftime('%d-%m-%Y')
        now = datetime.datetime.strptime(now, '%d-%m-%Y')
        sql.cur.execute(f"SELECT until FROM users WHERE id = '{message.from_user.id}'")
        until = datetime.datetime.strptime(sql.cur.fetchone()[0], '%d-%m-%Y')
        if now < until:
            await message.answer("Успешная авторизация", reply_markup=kb.menu)
            sql.db.close()
            await state.finish()
        else:
            await message.answer("Подписка неактивна, обратитесь к администратору, чтобы продлить подписку", reply_markup=kb.reg_menu)
            sql.db.close()
            await state.finish()

async def reg_name(message: types.Message, state: FSMContext):
    # Сохранение значения состояния ключ: значение
    #await state.update_data(name=message.text.lower())
    sql = DateBase()
    print(os.path)

    await state.update_data(name=message.text)
    user_data = await state.get_data()
    print(f"Ваше имечко {user_data['name']}")
    sql.cur.execute(f"SELECT dogovor FROM users WHERE name = '{user_data['name']}'")
    print(sql.cur.fetchone())
    sql.cur.execute(f"SELECT dogovor FROM users WHERE name = '{user_data['name']}'")
    res = str(sql.cur.fetchone()[0])


    if res == "org":
        await message.answer("Напишите телефонный номер парка, начиная с 8", reply_markup=kb.sub_menu)
    elif res == "ip":
        await message.answer("Напишите свой телефонный номер, зарегистрированный в КИС АРТ, начиная с 8", reply_markup=kb.sub_menu)
    await States.wait_reg_ph_number.set()

async def reg_number(message: types.Message, state: FSMContext):
    if len(message.text.lower()) != 11:
        await message.answer("Телефонный номер должен состоять из 11 символов")
        return
    await state.update_data(phone=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f"Ваше ФИО {user_data['name']}, номер телефона {user_data['phone']}", reply_markup=kb.sub_menu)
    name = user_data['name']
    sql = DateBase()
    sql.cur.execute(f"SELECT name FROM users WHERE name = '{name}'")
    print(name)

    string = sql.cur.fetchone()
    print(string)
    if string is None:
        await message.answer(f"Пользователь {name} не зарегистрирован, обратитесь к администратору", reply_markup=kb.reg_menu)
        await state.finish()
    else:
        sql.cur.execute(f"UPDATE users SET id = '{message.from_user.id}' WHERE name = '{name}'")
        sql.db.commit()
        await message.answer(f"Пользователь {name} зарегистрирован", reply_markup=kb.menu)
        sql.db.close()
        await state.finish()

async def check_status(message: types.Message, state: FSMContext):
    sql = DateBase()
    sql.cur.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if sql.cur.fetchone() is None:
        await message.answer(f"Вы не авторизованы, зарегистрируйтесь", reply_markup=kb.reg_menu)
        return
    sql.cur.execute(f"SELECT until FROM users WHERE id = '{message.from_user.id}'")
    until = datetime.datetime.strptime(sql.cur.fetchone()[0], '%d-%m-%Y')
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    now = datetime.datetime.strptime(now, '%d-%m-%Y')
    if (now < until) == True:
        print("Подписка активна")
        sql.db.close()
        pass
    else:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        print("Подписка не активна")
        sql.db.close()
        return
    sql_1 = DateBase()
    sql_1.cur.execute(f"SELECT status FROM users WHERE id = '{message.from_user.id}'")
    status = str(sql_1.cur.fetchone()[0])
    if status == "true":
        await message.answer("Путевой лист закрыт")
    elif status == "false":
        await message.answer("Путевой лист открыт")
        await state.finish()
        sql_1.db.close()
        return
    await state.finish()
    sql.db.close()

async def start_change_probeg(message: types.Message):
    sql = DateBase()
    sql.cur.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if sql.cur.fetchone() is None:
        await message.answer(f"Вы не авторизованы, зарегистрируйтесь", reply_markup=kb.reg_menu)
        return

    sql.cur.execute(f"SELECT until FROM users WHERE id = '{message.from_user.id}'")
    until = datetime.datetime.strptime(sql.cur.fetchone()[0], '%d-%m-%Y')
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    now = datetime.datetime.strptime(now, '%d-%m-%Y')
    if (now < until) == True:
        print("Подписка активна")
        sql.db.close()
        pass
    else:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку", reply_markup=kb.reg_menu)
        print("Подписка не активна")
        sql.db.close()
        return


    await message.answer("Напишите ваш текущий пробег", reply_markup=kb.sub_menu)
    await States.wait_start_weybills.set()

async def start_check(message: types.Message, state: FSMContext):
    await state.update_data(probeg=message.text.lower())
    user_data = await state.get_data()
    probeg = user_data['probeg']

    await message.answer("Проверка статуса", reply_markup=kb.sub_menu)
    url_login = 'https://art.taxi.mos.ru/login'
    url_waybills = 'https://art.taxi.mos.ru/waybills'

    sql = DateBase()

    sql.cur.execute(f"SELECT phone_number FROM users WHERE id = '{message.from_user.id}'")
    phone_nubmer = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT password FROM users WHERE id = '{message.from_user.id}'")
    password = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT dogovor FROM users WHERE id = '{message.from_user.id}'")
    dogovor = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT name FROM users WHERE id = '{message.from_user.id}'")
    name = sql.cur.fetchone()[0]


    print(f"Номер телефона {phone_nubmer}")
    print(f"ID {message.from_user.id}")
    print(f"Имя пользователя {name}")
    print(f"Пароль {password}")
    print(f"Пробег {probeg}")

    # Проверка статуса путевого листа
    sql.cur.execute(f"SELECT status FROM users WHERE id = '{message.from_user.id}'")
    status = str(sql.cur.fetchone()[0])
    if status == "true":
        await message.answer("Открытие смены")
        pass
    elif status == "false":
        await message.answer("Закройте смену, прежде чем открывать новую")
        await state.finish()
        sql.db.close()
        return

    # Проверка времени
    await message.answer("Проверка времени прошедшего с последней смены", reply_markup=kb.sub_menu)

    stat = datetime.timedelta(hours=12)

    sql.cur.execute(f"SELECT end_at FROM users WHERE id = '{message.from_user.id}'")
    end_time = datetime.datetime.strptime(sql.cur.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')
    now_time = datetime.datetime.now()
    delta = now_time - end_time
    if (delta > stat) == True:
        print("Пользователь отдохнул")
        await message.answer("С последней смены прошло более 12 часов")
    else:
        await message.answer("С последней смены не прошло более 12 часов, удаление путевого листа")
        print("Пользователь не отдыхал 12 часов")
        # Авторизация в Парке
        web = Web()
        await web.get_page(url_login)
        await web.set_form_input("msisdn", phone_nubmer)
        await web.set_form_input_enter("password", password)

        # Проверка корректного входа в ЛК
        if await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
            print("Удачная авторизация в ЛК пользователя")
            pass
        elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
            print("Неудалось авторизоваться в ЛК пользователя")
            await message.answer("Произошла ошибка при попытке авторизоваться в ЛК, повторите попытку через 1 минуту")
            await state.finish()
            web.browser.quit()
            sql.db.close()

        # Поиск старого путевого листа
        await web.get_page(url_waybills)
        await web.input_search(name.split(" ")[0])
        await web.choose_first()
        await web.click_button_only_text("span", "Удалить 1 запись")
        await web.click_button_only_text("span", "Oк")
        await message.answer("Путевой лист удален", reply_markup=kb.menu)
        web.browser.quit()

    sql.cur.execute(f"UPDATE users SET probeg = {probeg} WHERE id = '{message.from_user.id}'")
    sql.db.commit()
    if dogovor == "org":
        await message.answer("Подтвердите создание путевого листа", reply_markup=kb.sub_menu_org)
        await States.wait_start_org.set()
    elif dogovor == "ip":
        await message.answer("Подтвердите прохождение предрейсового осмотра", reply_markup=kb.sub_menu_ip)
        await States.wait_start_ip.set()

async def start_weybills_org(message: types.Message, state: FSMContext):
    await message.answer("Путевой лист в процессе создания", reply_markup=kb.sub_menu)
    print(__name__)
    url_login    = 'https://art.taxi.mos.ru/login'
    url_waybills = 'https://art.taxi.mos.ru/waybills'
    url_checkup  = "https://art.taxi.mos.ru/checkups"
    med_login    = "89257169519"
    med_passw    = "1bRoSb1P"
    mech_login   = "89773981068"
    mech_passw   = "1HoEcX0Q"

    sql = DateBase()


    sql.cur.execute(f"SELECT phone_number FROM users WHERE id = '{message.from_user.id}'")
    phone_nubmer = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT password FROM users WHERE id = '{message.from_user.id}'")
    password = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT probeg FROM users WHERE id = '{message.from_user.id}'")
    probeg = str(sql.cur.fetchone()[0])
    sql.cur.execute(f"SELECT name FROM users WHERE id = '{message.from_user.id}'")
    name = sql.cur.fetchone()[0]



    print(f"Номер телефона {phone_nubmer}")
    print(f"ID {message.from_user.id}")
    print(f"Имя пользователя {name}")
    print(f"Пароль {password}")
    print(f"Пробег {probeg}")

    # Авторизация в Парке
    web = Web()
    await web.get_page(url_login)
    await web.set_form_input("msisdn", phone_nubmer)
    await web.set_form_input_enter("password", password)

    # Проверка корректного входа в ЛК
    if await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК пользователя")
        pass
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК пользователя")
        await message.answer("Произошла ошибка при попытке авторизоваться в ЛК, повторите попытку через 1 минуту")
        await state.finish()
        web.browser.quit()
        sql.db.close()
        return

    # Создание путевого листа
    await web.get_page(url_waybills)
    await web.click_button_with_text("span", "MuiButton-label", "Добавить")
    await web.wait_page_load()
    # Ввод данных пользователя
    await web.set_form_input_enter_click("driver.id", name)
    time.sleep(10)
    await web.click_button_with_text("span", "MuiButton-label", "Сохранить")
    await web.wait_page_load()

    # Проверка создания путевого листа
    if await web.resource_check("MuiTypography-root MuiTypography-body1", "Создан путевой лист") == True:
        print("Путевой лист создан")
        await message.answer("Путевой лист создан")

        #Обновление статуса
        sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{message.from_user.id}'")
        sql.db.commit()

        pass
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Данные сохранены") == True:
        print("Путевой лист создан")
        await message.answer("Путевой лист создан")

        #Обновление статуса
        sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{message.from_user.id}'")
        sql.db.commit()

        pass
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Создан путевой лист") == False:
        print("Неудалось создать путевой лист")
        await message.answer("Произошла ошибка при при создании путевого листа, повторите попытку через 1 минуту", reply_markup=kb.menu)
        await state.finish()
        web.browser.quit()
        sql.db.close()
        return
    elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Данные сохранены") == False:
        print("Неудалось создать путевой лист")
        await message.answer("Произошла ошибка при при создании путевого листа, повторите попытку через 1 минуту", reply_markup=kb.menu)
        await state.finish()
        web.browser.quit()
        sql.db.close()
        return


    # Авторизация в ЛК Медика
    await message.answer("Прохождение предрейсового медосмотра")
    print("Авторзация медика")
    web_med = Web()
    await web_med.get_page(url_login)
    await web_med.set_form_input("msisdn", med_login)
    await web_med.set_form_input_enter("password", med_passw)

    # Проверка удачной авторизации в ЛК Медика
    if await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК медика")
        pass
    elif await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК медика")
        await message.answer("Произошла ошибка при прохождени предрейсового медосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_med.browser.quit()
        sql.db.close()
        return

    time.sleep(5)

    # Поиск созданного путевого листа
    await web_med.get_page(url_checkup)
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
    done_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

    # Проверка удачного одобрения листа
    if await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == True:
        print("Путевой лист удачно одобрен медиком")
        pass
    elif await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == False:
        print("Неудалось одобрить лист медиком")
        await message.answer("Произошла ошибка при прохождени предрейсового медосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_med.browser.quit()
        sql.db.close()
        return
    await message.answer(f"Предрейсовый медосмотр пройден в {done_time}, мед. работник - Ворфоломеева Н.А.")

    # Задержка
    #time.sleep(random.randint(4, 9))


    # Авторизация в ЛК Механика
    await message.answer("Прохождение предрейсового техосмотра")
    print("Авторзация механика")
    web_mech = Web()
    await web_mech.get_page(url_login)
    await web_mech.set_form_input("msisdn", mech_login)
    await web_mech.set_form_input_enter("password", mech_passw)

    # Проверка авторизации в ЛК Механика
    if await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК механика")
        pass
    elif await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК механика")
        await message.answer("Произошла ошибка при прохождени предрейсового техосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_mech.browser.quit()
        sql.db.close()
        return

    # Поиск путевого листа
    time.sleep(10)
    await web_mech.get_page(url_checkup)
    await web_mech.set_form_input_enter("publicId", name.split(" ")[0])

    await web_mech.hover_click("MuiTableRow-root")
    await web_mech.svg_click()

    await web_mech.set_form_input("checkupData.odometerData", probeg)
    await web_mech.input_checkox("checkupData.desinfected")
    await web_mech.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    done_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    done_time_db = datetime.datetime.now()

    # Провера удачного одобрения путевого листа
    if await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == True:
        print("Путевой лист удачно одобрен механиком")
        pass
    elif await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == False:
        print("Неудалось одобрить лист механиком")
        await message.answer("Произошла ошибка при прохождени предрейсового техосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_mech.browser.quit()
        sql.db.close()
        return
    await message.answer(f"Предрейсовый техосмотр пройден в {done_time}, механик - Соколов Е.А.")
    await message.answer("Выезд разрешен", reply_markup=kb.menu)

    # Обновить время начала смены ( считается от одобрения механика )
    sql.cur.execute(f"UPDATE users SET start_at = '{done_time_db}' WHERE id = '{message.from_user.id}'")
    sql.db.commit()

    # Закрытие драйверов, БД и состояний
    web_med.browser.quit()
    web_mech.browser.quit()
    web.browser.quit()
    sql.db.close()
    await state.finish()

async def start_weybills_ip(message: types.Message, state: FSMContext):
    print(__name__)
    url_login = 'https://art.taxi.mos.ru/login'
    url_checkup = "https://art.taxi.mos.ru/checkups"
    med_login = "89257169519"
    med_passw = "1bRoSb1P"
    mech_login = "89773981068"
    mech_passw = "1HoEcX0Q"

    sql = DateBase()

    sql.cur.execute(f"SELECT phone_number FROM users WHERE id = '{message.from_user.id}'")
    phone_nubmer = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT password FROM users WHERE id = '{message.from_user.id}'")
    password = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT probeg FROM users WHERE id = '{message.from_user.id}'")
    probeg = str(sql.cur.fetchone()[0])
    sql.cur.execute(f"SELECT name FROM users WHERE id = '{message.from_user.id}'")
    name = sql.cur.fetchone()[0]

    print(f"Номер телефона {phone_nubmer}")
    print(f"ID {message.from_user.id}")
    print(f"Имя пользователя {name}")
    print(f"Пароль {password}")
    print(f"Пробег {probeg}")

    # Обновление статуса
    sql.cur.execute(f"UPDATE users SET status = 'false' WHERE id = '{message.from_user.id}'")
    sql.db.commit()

    # Авторизация в ЛК Медика
    await message.answer("Прохождение предрейсового медосмотра")
    print("Авторзация медика")
    web_med = Web()
    await web_med.get_page(url_login)
    await web_med.set_form_input("msisdn", med_login)
    await web_med.set_form_input_enter("password", med_passw)

    # Проверка удачной авторизации в ЛК Медика
    if await web_med.resource_check("MuiTypography-root MuiTypography-body1",
                                    "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК медика")
        pass
    elif await web_med.resource_check("MuiTypography-root MuiTypography-body1",
                                      "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК медика")
        await message.answer(
            "Произошла ошибка при прохождени предрейсового медосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_med.browser.quit()
        sql.db.close()
        return

    time.sleep(5)

    # Поиск созданного путевого листа
    await web_med.get_page(url_checkup)
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
    done_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

    # Проверка удачного одобрения листа
    if await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == True:
        print("Путевой лист удачно одобрен медиком")
        pass
    elif await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == False:
        print("Неудалось одобрить лист медиком")
        await message.answer(
            "Произошла ошибка при прохождени предрейсового медосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_med.browser.quit()
        sql.db.close()
        return
    await message.answer(f"Предрейсовый медосмотр пройден в {done_time}, мед. работник - Ворфоломеева Н.А.")

    # Задержка
    # time.sleep(random.randint(4, 9))

    # Авторизация в ЛК Механика
    await message.answer("Прохождение предрейсового техосмотра")
    print("Авторзация механика")
    web_mech = Web()
    await web_mech.get_page(url_login)
    await web_mech.set_form_input("msisdn", mech_login)
    await web_mech.set_form_input_enter("password", mech_passw)

    # Проверка авторизации в ЛК Механика
    if await web_mech.resource_check("MuiTypography-root MuiTypography-body1",
                                     "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК механика")
        pass
    elif await web_mech.resource_check("MuiTypography-root MuiTypography-body1",
                                       "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК механика")
        await message.answer(
            "Произошла ошибка при прохождени предрейсового техосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_mech.browser.quit()
        sql.db.close()
        return

    # Поиск путевого листа
    time.sleep(10)
    await web_mech.get_page(url_checkup)
    await web_mech.set_form_input_enter("publicId", name.split(" ")[0])

    await web_mech.hover_click("MuiTableRow-root")
    await web_mech.svg_click()

    await web_mech.set_form_input("checkupData.odometerData", probeg)
    await web_mech.input_checkox("checkupData.desinfected")
    await web_mech.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    done_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    done_time_db = datetime.datetime.now()

    # Провера удачного одобрения путевого листа
    if await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == True:
        print("Путевой лист удачно одобрен механиком")
        pass
    elif await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Добавлен осмотр") == False:
        print("Неудалось одобрить лист механиком")
        await message.answer(
            "Произошла ошибка при прохождени предрейсового техосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_mech.browser.quit()
        sql.db.close()
        return
    await message.answer(f"Предрейсовый техосмотр пройден в {done_time}, механик - Соколов Е.А.")
    await message.answer("Выезд разрешен", reply_markup=kb.menu)

    # Обновить время начала смены ( считается от одобрения механика )
    sql.cur.execute(f"UPDATE users SET start_at = '{done_time_db}' WHERE id = '{message.from_user.id}'")
    sql.db.commit()

    # Закрытие драйверов, БД и состояний
    web_med.browser.quit()
    web_mech.browser.quit()
    sql.db.close()
    await state.finish()

async def end_change_probeg(message: types.Message):
    sql = DateBase()
    sql.cur.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if sql.cur.fetchone() is None:
        await message.answer(f"Вы не авторизованы, зарегистрируйтесь", reply_markup=kb.reg_menu)
        return

    sql.cur.execute(f"SELECT until FROM users WHERE id = '{message.from_user.id}'")
    until = datetime.datetime.strptime(sql.cur.fetchone()[0], '%d-%m-%Y')
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    now = datetime.datetime.strptime(now, '%d-%m-%Y')
    if (now < until) == True:
        print("Подписка активна")
        sql.db.close()
        pass
    else:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        print("Подписка не активна")
        sql.db.close()
        return
    await message.answer("Напишите ваш текущий пробег", reply_markup=kb.sub_menu)
    await States.wait_end_weybills.set()

async def end_weybills(message: types.Message, state: FSMContext):
    await state.update_data(probeg=message.text.lower())
    user_data = await state.get_data()
    probeg = user_data['probeg']
    sql = DateBase()
    sql.cur.execute(f"UPDATE users SET probeg = {probeg} WHERE id = '{message.from_user.id}'")
    sql.db.commit()
    await message.answer(f"Пробег обновлен", reply_markup=kb.sub_menu)

    url_login = 'https://art.taxi.mos.ru/login'
    url_checkup = "https://art.taxi.mos.ru/checkups"
    med_login = "89257169519"
    med_passw = "1bRoSb1P"
    mech_login = "89773981068"
    mech_passw = "1HoEcX0Q"


    sql.cur.execute(f"SELECT probeg FROM users WHERE id = '{message.from_user.id}'")
    probeg = str(sql.cur.fetchone()[0])
    sql.cur.execute(f"SELECT name FROM users WHERE id = '{message.from_user.id}'")
    name = sql.cur.fetchone()[0]

    print(f"ID {message.from_user.id}")
    print(f"Имя пользователя {name}")
    print(f"Пробег {probeg}")

    # Авторизация в ЛК Медика
    await message.answer("Прохождение послерейсового медосмотра")
    print("Авторзация медика")
    web_med = Web()
    await web_med.get_page(url_login)
    await web_med.set_form_input("msisdn", med_login)
    await web_med.set_form_input_enter("password", med_passw)

    # Проверка удачной авторизации в ЛК Медика
    if await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК медика")
        pass
    elif await web_med.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК медика")
        await message.answer("Произошла ошибка при прохождении послерейсового медосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_med.browser.quit()
        sql.db.close()


    # Поиск созданного путевого листа
    time.sleep(5)
    await web_med.get_page(url_checkup)
    await web_med.set_form_input_enter("publicId", name.split(" ")[0])
    cl_1 = "MuiTableRow-root"
    await web_med.hover_click(cl_1)

    # Закрытие осмотра
    #await web_med.click_button_role()
    await web_med.svg_click()
    await web_med.input_checkox("checkupData.alcoholTestPassed")
    await web_med.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    await message.answer(f"Послерейсовый медосмотр пройден в {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}, мед. работник - Ворфоломеева Н.А.")



    # Авторизация в ЛК Механика
    await message.answer("Прохождение послерейсового техосмотра")
    print("Авторзация механика")
    web_mech = Web()
    await web_mech.get_page(url_login)
    await web_mech.set_form_input("msisdn", mech_login)
    await web_mech.set_form_input_enter("password", mech_passw)

    # Проверка авторизации в ЛК Механика
    if await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
        print("Удачная авторизация в ЛК механика")
        pass
    elif await web_mech.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
        print("Неудалось авторизоваться в ЛК механика")
        await message.answer("Произошла ошибка при прохождении послерейсового техосмотра, удалите лист и повторите попытку через 1 минуту")
        await state.finish()
        web_mech.browser.quit()
        sql.db.close()

    # Поиск путевого листа
    time.sleep(5)
    await web_mech.get_page(url_checkup)
    await web_mech.set_form_input_enter("publicId", name.split(" ")[0])
    cl_1 = "MuiTableRow-root"
    await web_mech.hover_click(cl_1)

    # Закрытие осмотра
    #await web_mech.click_button_role()
    await web_mech.svg_click()
    await web_mech.set_form_input("checkupData.odometerData", probeg)
    await web_mech.input_checkox("checkupData.washed")
    await web_mech.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")
    await message.answer(f"Послерейсовый техосмотр пройден в {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}, механик - Соколов Е.А.")
    await message.answer("Смена закрыта", reply_markup=kb.menu)

    #Обновление статуса
    sql.cur.execute(f"UPDATE users SET status = 'true' WHERE id = '{message.from_user.id}'")
    sql.db.commit()


    # Обновить время конца смены ( считается от одобрения механика )
    sql.cur.execute(f"UPDATE users SET end_at = '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}' WHERE id = '{message.from_user.id}'")
    sql.db.commit()

    # Закрытие драйверов, БД и состояний
    web_med.browser.quit()
    web_mech.browser.quit()
    sql.db.close()
    await state.finish()

async def delete_weybills(message: types.Message, state: FSMContext):
    sql = DateBase()
    sql.cur.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if sql.cur.fetchone() is None:
        await message.answer(f"Вы не авторизованы, зарегистрируйтесь", reply_markup=kb.reg_menu)
        return

    sql.cur.execute(f"SELECT until FROM users WHERE id = '{message.from_user.id}'")
    until = datetime.datetime.strptime(sql.cur.fetchone()[0], '%d-%m-%Y')
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    now = datetime.datetime.strptime(now, '%d-%m-%Y')
    if (now < until) == True:
        print("Подписка активна")
        pass
    else:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        print("Подписка не активна")
        sql.db.close()
        return

    await message.answer("Проверка времени прошедшего с последней смены", reply_markup=kb.sub_menu)
    url_login = 'https://art.taxi.mos.ru/login'
    url_waybills = 'https://art.taxi.mos.ru/waybills'

    sql.cur.execute(f"SELECT phone_number FROM users WHERE id = '{message.from_user.id}'")
    phone_nubmer = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT password FROM users WHERE id = '{message.from_user.id}'")
    password = sql.cur.fetchone()[0]
    sql.cur.execute(f"SELECT name FROM users WHERE id = '{message.from_user.id}'")
    name = sql.cur.fetchone()[0]

    stat = datetime.timedelta(hours=12)
    cheat = datetime.timedelta(hours=13)
    sql.cur.execute(f"SELECT end_at FROM users WHERE id = '{message.from_user.id}'")
    end_time = datetime.datetime.strptime(sql.cur.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')
    now_time = datetime.datetime.now()
    delta = now_time - end_time
    if (delta > stat) == True:
        print("Пользователь отдохнул")
        await message.answer("С последней смены прошло более 12 часов", reply_markup=kb.menu)
        return
    else:
        print("Пользователь не отдыхал 12 часов")
        # Авторизация в Парке
        web = Web()
        await web.get_page(url_login)
        await web.set_form_input("msisdn", phone_nubmer)
        await web.set_form_input_enter("password", password)

        # Проверка корректного входа в ЛК
        if await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == False:
            print("Удачная авторизация в ЛК пользователя")
            pass
        elif await web.resource_check("MuiTypography-root MuiTypography-body1", "Неверное имя пользователя или пароль") == True:
            print("Неудалось авторизоваться в ЛК пользователя")
            await message.answer("Произошла ошибка при удалении путевого листа, повторите попытку через 1 минуту", reply_markup=kb.menu)
            await state.finish()
            web.browser.quit()
            sql.db.close()

        # Поиск старого путевого листа
        await web.get_page(url_waybills)
        await web.input_search(name[0:3])
        await web.choose_first()
        await web.click_button_only_text("span", "Удалить 1 запись")
        await web.click_button_only_text("span", "Oк")
        await message.answer("Путевой лист удален", reply_markup=kb.menu)
        await state.finish()
        web.browser.quit()
        sql.cur.execute(f"UPDATE users SET end_at = '{end_time - cheat}' WHERE id = '{message.from_user.id}'")
        sql.db.commit()
        sql.db.close()


async def cmd_cancel(message: types.Message, state: FSMContext):
    sql = DateBase()
    sql.cur.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if sql.cur.fetchone() is None:
        await message.answer(f"Вы не авторизованы, зарегистрируйтесь", reply_markup=kb.reg_menu)
        return
    sql.cur.execute(f"SELECT until FROM users WHERE id = '{message.from_user.id}'")
    until = datetime.datetime.strptime(sql.cur.fetchone()[0], '%d-%m-%Y')
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    now = datetime.datetime.strptime(now, '%d-%m-%Y')
    if (now < until) == True:
        print("Подписка активна")
        sql.db.close()
        pass
    else:
        await message.answer("Ваша подписка истекла, обратитесь к администратору что бы продлить подписку",
                             reply_markup=kb.reg_menu)
        print("Подписка не активна")
        sql.db.close()
        return

    await state.finish()
    await message.answer("Отмена", reply_markup=kb.menu)


def register_handlers_choose(dp: Dispatcher):


    dp.register_message_handler(check_id, Text(equals="Регистрация", ignore_case=True), state="*")
    dp.register_message_handler(reg_name, state=States.wait_reg_name)
    dp.register_message_handler(reg_number, state=States.wait_reg_ph_number)

    dp.register_message_handler(start_change_probeg, Text(equals="Начало смены", ignore_case=True), state="*")
    dp.register_message_handler(start_check, state=States.wait_start_weybills)

    dp.register_message_handler(start_weybills_ip, state=States.wait_start_ip)
    dp.register_message_handler(start_weybills_org, state=States.wait_start_org)

    dp.register_message_handler(check_status, Text(equals="Статус путевого листа", ignore_case=True), state="*")
    dp.register_message_handler(end_change_probeg, Text(equals="Закрыть смену", ignore_case=True), state="*")
    dp.register_message_handler(end_weybills, state=States.wait_end_weybills)
    dp.register_message_handler(delete_weybills, Text(equals="Удалить лист", ignore_case=True), state="*")

    dp.register_message_handler(cmd_cancel, Text(equals="Отменить", ignore_case=True), state="*")









