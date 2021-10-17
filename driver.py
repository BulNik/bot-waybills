import time
import json
# Импорт вебдрайвера - основной библиотеки для работы с браузером
from selenium import webdriver

# Импорт ключей, которые соответствуют клавишам на клавиатуре
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

class Web():
    def __init__(self):
        # Инциируем объект опций для Хрома, чтобы иметь возможность подключить расширение
        options = webdriver.ChromeOptions()
        #options.add_argument("user-data-dir=selenium")
        options.add_argument('--headless')
        # Запускаем Браузер (Веб Драйвер Хрома) с указанием места скачивания самого файла драйвера
        self.browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=options, service_args=["--verbose", "--log-path=chrome.log"])

    async def get_page(self, url):
        self.browser.get(url)

    async def click_button(self, selector, cl):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//"{selector}"[@class="{cl}"]')))
        elem = self.browser.find_elements_by_xpath(f'//"{selector}"[@class="{cl}"]')[0]
        elem.click()
        time.sleep(5)

    async def click_button_only_text(self, selector, text):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//{selector}[text()="{text}"]')))
        elem = self.browser.find_element_by_xpath(f'//{selector}[text()="{text}"]')
        elem.click()
        time.sleep(10)

    async def click_button_with_text(self, selector, cl, text):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//{selector}[@class="{cl}" and text()="{text}"]')))
        elem = self.browser.find_element_by_xpath(f'//{selector}[@class="{cl}" and text()="{text}"]')
        elem.click()
        time.sleep(10)

    async def click_button_with_text_and_div(self, selector, cl, text):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//div[@role="dialog"]//{selector}[@class="{cl}" and text()="{text}"]')))
        elem = self.browser.find_element_by_xpath(f'//div[@role="dialog"]//{selector}[@class="{cl}" and text()="{text}"]')
        elem.click()
        time.sleep(10)

    async def set_form_input(self, selector_name, text):
        print("Отправка в форму ")
        print(text)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//input[@name="{selector_name}"]')))
        elem = self.browser.find_element_by_xpath(f'//input[@name="{selector_name}"]')
        elem.send_keys(text)

    async def set_form_input_enter(self, selector_name, text):
        print("Отправка в форму и ввод")
        print(text)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//input[@name="{selector_name}"]')))
        elem = self.browser.find_element_by_xpath(f'//input[@name="{selector_name}"]')
        elem.send_keys(text)
        elem.send_keys(Keys.ENTER)

    async def set_form_input_enter_click(self, selector_name, text: str):
        name = text.title()
        print(name)
        tr = 0
        try:
            print(f"Попытка  {tr}")
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//input[@name="{selector_name}"]')))
            elem = self.browser.find_element_by_xpath(f'//input[@name="{selector_name}"]')
            elem.click()
            WebDriverWait(self.browser, 10).until( EC.presence_of_element_located((By.XPATH, f'//li[@role="option" and @class="MuiAutocomplete-option" and text()="{name}"]')))
            elem_2 = self.browser.find_element_by_xpath(f'//li[@role="option" and @class="MuiAutocomplete-option" and text()="{name}"]')
            elem_2.click()
            print("нажали")
            time.sleep(5)
            print(f"{name} {elem.get_attribute('value')}")
            if name in elem.get_attribute('value'):
                print("Имя введено корректно")
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                    (By.XPATH, f'//span[@class="MuiButton-label" and text()="Сохранить"]')))
                elem_3 = self.browser.find_element_by_xpath(
                    f'//span[@class="MuiButton-label" and text()="Сохранить"]')
                elem_3.click()
                print("лик по сохраняшке")

                return
        except:
            print("Не найдено в первой итерации")

        while tr < 3:
            tr += 1
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//input[@name="{selector_name}"]')))
            elem = self.browser.find_element_by_xpath(f'//input[@name="{selector_name}"]')
            elem.send_keys(name.split(" ")[0])
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, f'//li[@role="option" and @class="MuiAutocomplete-option" and text()="{name}"]')))
            elem_2 = self.browser.find_element_by_xpath(
                f'//li[@role="option" and @class="MuiAutocomplete-option" and text()="{name}"]')
            elem_2.click()
            if name in elem.get_attribute('value'):
                print("Имя введено корректно")
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                    (By.XPATH, f'//span[@class="MuiButton-label" and text()="Сохранить"]')))
                elem_3 = self.browser.find_element_by_xpath(
                    f'//span[@class="MuiButton-label" and text()="Сохранить"]')
                elem_3.click()
                print("лик по сохраняшке")

                return





            #print("clear")
            #elem.clear()
            #time.sleep(5)
            #elem.send_keys(text.split(" ")[0])
            #print("Ввели текст")
            #time.sleep(5)



            #web_mech.click_button_with_text_and_div("span", "MuiButton-label", "Сохранить")



    async def check_text_input(self, name):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//input[@name="driver.id"]')))
        elem = self.browser.find_element_by_xpath(f'//input[@name="driver.id"]')
        if name in str.lower(elem.text):
            print(str.lower(elem.text))
            print("нашел имя")
            status = True
            return status
        else:
            print("нашел имя")
            status = False
            return

    async def hover_click(self, cl_1):
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, f'//button[@title="Редактировать путевой лист"]')))
        elem = self.browser.find_elements_by_xpath(f'//button[@title="Редактировать путевой лист"]//span[text()="edit"]')[0]
        hover = ActionChains(self.browser).move_to_element(elem)
        hover.perform()
        time.sleep(1)
        elem.click()
        self.browser.find_elements_by_xpath(f'//span[text()="edit"]')[0].click()

    async def svg_click(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[name()="svg"][@class="MuiSvgIcon-root MuiSvgIcon-fontSizeSmall"]')))
        self.browser.find_elements_by_xpath(f'//*[name()="svg"][@class="MuiSvgIcon-root MuiSvgIcon-fontSizeSmall"]')[1].click()

    async def svg_click_2(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[name()="svg"][@class="MuiSvgIcon-root MuiSvgIcon-fontSizeSmall"]')))
        self.browser.find_elements_by_xpath(f'//*[name()="svg"][@class="MuiSvgIcon-root MuiSvgIcon-fontSizeSmall"]')[2].click()

    async def resource_check(self, cl, text):
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//p[@class="{cl}" and text()="{text}"]')))
            check_stat = True
            return check_stat
        except:
            check_stat = False
            return check_stat


    async def click_button_role(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//span[@role="button"]')))
        self.browser.find_elements_by_xpath(f'//span[@role="button"]')[2].click()

    async def input_checkox(self, cl):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//input[@name="{cl}"]')))
        self.browser.find_element_by_xpath(f'//input[@name="{cl}"]').click()


    async def wait_page_load(self):
        while self.browser.execute_script('return document.readyState;') != 'complete':
            time.sleep(5)

    async def input_search(self, text):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Искать"]')))
        elem = self.browser.find_element_by_xpath(f'//input[@placeholder="Искать"]')
        elem.send_keys(text)
        elem.send_keys(Keys.ENTER)

    async def choose_first(self):
        #WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="MuiIconButton-label"]')))
        #self.browser.find_elements_by_xpath('//span[@class="MuiIconButton-label"]')[2].click()

        #input[@value='0']
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@value="0"]')))
        self.browser.find_element_by_xpath('//input[@value="0"]').click()

        #(//*[name()='svg'][@class='MuiSvgIcon-root'])[1]
        #WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[name()="svg"][@class="MuiSvgIcon-root"]')))
        #self.browser.find_elements_by_xpath('//*[name()="svg"][@class="MuiSvgIcon-root"]')[1].click()

#//span[contains(text(),'Удалить 1 запись')]


