from bs4 import BeautifulSoup
import requests
from requests.models import parse_header_links
import re
import time
import random

# url = 'https://www.citilink.ru/product/garnitura-vkladyshi-edifier-tws-nb2-pro-seryi-besprovodnye-bluetooth-1541318'

def get_tech_page(url, headers): #Получаем всё содержимое страниц по ссылкам, добавляем в список.
    # time.sleep(15) #Для теста.
    timeout = random.randrange(46,72)
    time.sleep(timeout) #Для рабочего запуска
    print('Get: ' + url, 'Таймаут', timeout, 'сек.' )
    resp = requests.get(url + '/properties/', headers=headers)
    page_soup = BeautifulSoup(resp.text, 'lxml')
    return page_soup


def get_spec(page_soup):
    spec_info_table = page_soup.find('div', class_='js--TabContent TabContent Tabs__content')
    return spec_info_table


def get_acoustic(table):
    try:
        rows = table.find_all('div', class_='Specifications__row')
    except AttributeError as err:
        print(table)
        print('Не надены строки спецификации, пропускаем')
        return 'None'
    # print(rows)
    return rows


def get_acoustic_spec(rows): #Получаем со страницы значение акустического диапазона в виде списка из двух элеменов, заголовок - значение.
    acoustic_spec = []
    for el in rows:
        # print(el)
        try:
            name = el.find('div', class_='Specifications__column_name')
        except TypeError as err:
            print('Нет колонки, пропускаем')
            name = None
        try:
            name_clean = re.sub("^\s+|\n|\r|\s+$", '', name.text)
            # print(name_clean)
        except AttributeError as err:
                name_clean = None
        if name_clean == 'Диапазон воспроизводимых частот':
            # print(name_clean)
            acoustic_spec.append(name_clean)
            value = el.find('div', class_='Specifications__column_value')
            value_clean = re.sub("^\s+|\n|\r|\s+$", '', value.text)
            # print(value_clean)
            acoustic_spec.append(value_clean)
    print(acoustic_spec)
    return acoustic_spec
