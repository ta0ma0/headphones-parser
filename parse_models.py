from bs4 import BeautifulSoup
import requests
import os.path
import re
from get_tech_info import get_tech_page, get_spec, get_acoustic, get_acoustic_spec
import time
import csv
import json


https_proxy = 'https://170.238.255.90:31113'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) ',
}
proxyDict = {"https": https_proxy}
home = 'https://www.citilink.ru'
url = 'https://www.citilink.ru/catalog/naushniki/?f=discount.any%2Crating.any%2C11965_240%2C7268_240%2C7281_240besprovodnyed1bluetooth&price_max=25000&pf=discount.any%2Crating.any%2C11965_240%2C7268_240&price_min=3000&pprice_max=25000&pprice_min=3000&sorting=price_desc'

if not os.path.isfile('index.html'):
    response = requests.get(url)
    with open('index.html', 'w') as f:
        f.write(response.text)
else:
    print('File exist')


with open('index.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
main_div = soup.main.section

product_carts = main_div.find_all('div', class_="ProductCardVerticalLayout")


def get_productcarts_from_page(urls):
    contents = requests.get(urls)
    soup = BeautifulSoup(contents.text, 'lxml')
    main_div_ = soup.main.section
    product_carts = main_div_.find_all(
        'div', class_="ProductCardVerticalLayout")
    return product_carts


def get_prod_price(product_carts):
    price_prod = []
    for el in product_carts:
        price_prod_pair = []
        link = el.find('a', class_='ProductCardVertical__name', href=True)
        price = el.find(
            'span', class_='js--ProductCardVerticalPrice__price-current_current-price')
        try:
            price = re.sub("^\s+|\n|\r|\s+$", '', price.text)
        except AttributeError as err:
            price = 'None'
        link_text = re.sub("^\s+|\n|\r|\s+$", '', link.text)
        price_prod_pair.append(link_text)
        price_prod_pair.append(price)
        price_prod_pair.append(link['href'])
        price_prod.append(price_prod_pair)
    return price_prod


def get_pages(main_div):
    paginator = main_div.find(
        'div', class_='ProductCardCategoryList__pagination')
    links = []
    page_link = paginator.find_all(
        'a', class_='js--PaginationWidget__page', href=True)
    for el in page_link:
        links.append(el['href'])
    return links


# Получаем линки и цены со страниц пагинатора, создаем список списков, чтобы потом его смержить с main_page_prod_price
links = get_pages(main_div)  # Получаем список URL из пагинатора.
# Переменная для списка ссылок и цены с кажой страницы из пагинатора
from_paginators_prod_price = []
result_prod_price = []
# main_page_cards = get_productcarts_from_page(
#     url)  # Получаем карточки товаров с главной

# print(main_page_cards)
from_main_prod_price = get_prod_price(product_carts)
# print(from_main_prod_price)
for el in from_main_prod_price:  # Получаем ссылки и цену с главной
    result_prod_price.append(el)


for url in links:
    print(url)
    prods_cards = get_productcarts_from_page(url)
    # Получаем данные (ссылки и цену) с пагинатора
    data = get_prod_price(prods_cards)
    time.sleep(1)
    from_paginators_prod_price.append(data)


for el in from_paginators_prod_price: #Добавляем данные к ссылкам с главной из пагинатора.
    # print(el)
    for el2 in el:
        result_prod_price.append(el2)


# Список ссылка и цена со всех товаров найденных по исходному фильтру.
# print(result_prod_price[0])

# Проходим по всем полученным страницам наушников в поисках характеристик и доплняем список с именем и ценой, акустическим диапазоном.
fields = ['Name', 'Acoustic', 'Price', 'Link']
end_result_table = []
counter = 0

with open('result_prod_price.json', 'w') as f:
    json.dump(result_prod_price, f)

#todo, сделать сохранение состояние и начала с прекращенной ссылки.

for el in result_prod_price:
    result_table = []
    url = el[2]
    tech_page_soup = get_tech_page(home + url, headers)
    # tech_page_soup = get_tech_page('https://www.citilink.ru/product/naushniki-s-mikrofonom-honor-magic-earbuds-tws-walrus-bluetooth-vklady-1376140/', headers=headers)
    spec_info_table = get_spec(tech_page_soup)
    tech_rows = get_acoustic(spec_info_table)
    acoustic_spec = get_acoustic_spec(tech_rows)
    result_table.append(el[0])
    result_table.append(acoustic_spec)
    result_table.append(el[1])
    result_table.append(home + url)
    counter +=1
    print('Осталось обработать ', len(result_prod_price) - counter)
    end_result_table.append(result_table)
    with open('headphones_2.csv', 'a') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(result_table)


# for el in end_result_table:
#     with open('headphones.csv', 'w', newline='\n') as myfile:
#         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#         wr.writerow(el)
#     print(el)




