import csv
import requests
import re
from bs4 import BeautifulSoup

urls_file='zashita-kartera.txt'
#urls_file='farkop.txt'


with open(urls_file) as file:
    urls = [row.strip() for row in file]

print(urls)

page=1
all_products = []
for url in urls:
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("div", {"class": "catalog-item"})
    page +=1
    print(len(products), 'стр:', page)
    for product in products:
        product_card = product.find("div", {"class": "catalog-item__summary"})
        name = product.find("h3", {"class": "catalog-item__head"}).text
        k = name.rfind('Артикул ')
        sku = name[k+8:]
        price = product.find("div", {"class": "catalog-item__price"}).text.strip().replace("₽", "")
        quantity = product.find("span", {"class": "catalog-item__quantity-count"})
        quantity = str(quantity)
        if len(quantity) >= 1:
            quantity = re.sub("[^0-9]", "", quantity)
            if len(quantity) == 0:
                quantity = 0

        all_products.append([name, sku, price, quantity])

        #names = ['Наименование', 'Артикул', 'Цена', 'Количество']

        out_file = urls_file.replace('txt','csv')


        with open(out_file, "w", encoding='cp1251', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            #writer.writerow(names)
            for product in all_products:
                writer.writerow(product)
print(out_file)
print('done')

