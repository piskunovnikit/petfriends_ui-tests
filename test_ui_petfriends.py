# pytest -v --driver Chrome --driver-path C:/chrome/chromedriver.exe

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome('C:/chrome/chromedriver.exe')
import time
import pytest

# подготавливаем тесты: авторизуемся, заходим на страницу с моими питомцами

def testing_preparation():

    # driver.implicitly_wait(5)
    driver.get('https://petfriends.skillfactory.ru/login')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys('lomnik1995@yandex.ru')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "pass"))).send_keys('qazwsxedc')
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Мои питомцы'))).click()
#
#     # driver.quit()

def test_check_count_pets():
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверяем, что на странице "Мои питомцы" присутствуют все питомцы
   # Из всей таблицы питомцев
    pets_list = driver.find_element(by=By.XPATH, value="//tbody")
   # Вычленяем список питомцев из этой таблицы, каждый из элементов лежит в тегах 'tr'
    pets_list_info = pets_list.find_elements(by=By.TAG_NAME, value='tr')
   # Добываем число, находящееся в блоке слева напротив слова "Питомцев: "
    number_of_pets = driver.find_element(By.XPATH, "(//div[@class='.col-sm-4 left'])[1]").text.replace("\n", "").split(": ")[1].split("Друзей")[0]
   # Убеждаемся, что мы добыли его верно
    print(number_of_pets)
    print(pets_list_info)
   # Сравниваем длину списка питомцев из таблицы с числом из блока слева
    assert len(pets_list_info) == int(number_of_pets)


def test_pets_list_have_photo():
   driver.get('https://petfriends.skillfactory.ru/my_pets')
   WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверяем, что на странице "Мои питомцы" присутствуют все питомцы
   # Из всей таблицы питомцев
   pets_list = driver.find_element(by=By.XPATH, value="//tbody")
   # Вычленяем список питомцев по тегу img
   pets_list_photo = pets_list.find_elements(by=By.TAG_NAME, value='img')
   # Считаем кол-во тех питомцев, у которых значение абрибута scr в теге img не равно нулю, то есть есть ссылка на фото
   counter = 0
   for i in pets_list_photo:
      if i.get_attribute('src') != "":
         counter += 1
   # Проверяем, что питомцев с фото больше либо равно половине всего списка питомцев с тегом img
   assert counter >= len(pets_list_photo) / 2, 'количество питомцев с фото меньше половины'




def test_all_pets_have_name_age_and_type():
    info_of_my_pets = driver.find_elements(by=By.TAG_NAME, value='div td')
    # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    # получаем имена, типы и возрасты питомцев
    names = info_of_my_pets[::4]
    types = info_of_my_pets[1::4]
    ages = info_of_my_pets[2::4]
    print(names)
    assert '' not in names, 'Не у всех питомцев есть имя'
    # проверяем, что у всех питомцев есть порода
    assert '' not in types, 'Не у всех питомцев есть порода'
    # проверяем, что у всех питомцев есть возраст
    count_noage = 0
    assert '' not in ages, 'Не у всех питомцев есть возраст'

def test_different_names():
    info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    names = info_of_my_pets[::4]
    # проверяем, что у всех питомцев разные имена
    assert len(names) == len(list(set(names))), 'В списке есть питомцы с разными именами'



def test_different_pets():

    info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    # удаляем из списка элементы-крестики (удалить питомца)
    del info_of_my_pets[::4]
    # группируем каждые три элемента списка питомцев в кортеж (имя,порода,возраст)
    info_of_my_pets_tuple=[tuple(info_of_my_pets[i:i+3]) for i in range (0,len(info_of_my_pets),3)]
    # проверяем, есть ли в списке кортежей одинаковые элементы
    assert len(info_of_my_pets_tuple)==len(list(set(info_of_my_pets_tuple))),'В списке есть повторяющиеся питомцы'
    driver.quit()
