"""
Скрипт парсинга данных с карточек товара сайта tachka.ru.
"""

# Импорт библиотек
import csv
import requests
import re
from bs4 import BeautifulSoup

# Подключаем файл с ссылками на страницы, которые нужно обойти
# Ссылки формируем отдельным скриптом и копируем в корень проекта

#urls_file='zashita-kartera.txt'
urls_file='farkop.txt'
#urls_file='kreplenie-dlya-velosipeda.txt'





# Шаг открывает для чтения файл с сылками и записывает их в массив
with open(urls_file) as file:
    urls = [row.strip() for row in file]

print(urls)

page=1 # Переменная для индекации номера сканируемой страницы
all_products = [] # массив для сохранения полученных с карточки данных
for url in urls: #
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("div", {"class": "catalog-item"}) # Получаем массив экземпляров карточки товара
    page +=1
    print(len(products), 'стр:', page)
    for product in products: # Открываем каждую карточку для парсинга
        # product_card = product.find("div", {"class": "catalog-item__summary"})
        category = soup.find_all("span", {"itemprop": "name"})
        category = str(category)
        category = re.sub("[^А-я, " "]", "", category)
        name = product.find("h3", {"class": "catalog-item__head"}).text # наименование продукта
        k = name.rfind('Артикул ') # переменная для вычисления позиции подстроки
        sku = name[k+8:] # значение артикула вырезаем из наименования
        price = product.find("div", {"class": "catalog-item__price"}).text.strip().replace("₽", "") # получаем значение цены и обрезаем лишние символы
        quantity = product.find("span", {"class": "catalog-item__quantity-count"}) # получаем значение остатка продукта
        quantity = str(quantity) # переопределяем тип значения остатка
        if len(quantity) >= 1: # очистка значекния данных остатка от лишних символов
            quantity = re.sub("[^0-9]", "", quantity) # удаление всех символов из строки, кроме цыфр
            if len(quantity) == 0: # если в количество ничего не записано, присваеваем ему значение 0
                quantity = 0
        specific = product.find("div", {"class": "catalog-item__attributes attributes"}).text.strip()
        specific = str(specific)
        specific = re.sub('\n|\s', '', specific)
        m = specific.rfind('ль:')
        manufacturer = specific[m+3:]
        all_products.append([name, sku, price, quantity, manufacturer, category]) # записываем полученные данные в массив

        #names = ['Наименование', 'Артикул', 'Цена', 'Количество']

        out_file = urls_file.replace('txt','csv') # создаём наименование файла выгрузки


        with open(out_file, "w", encoding='cp1251', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            #writer.writerow(names) # первая строка с заголовками столбцов
            for product in all_products: # Построчная запись в файл значений из массива
                writer.writerow(product)
print(out_file)
print('done')

