# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте во всех категориях:
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.

import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd

website = 'https://books.toscrape.com/'
url = website + 'catalogue/page-1.html'

p_count = 0 # для подсчета количества обработанных веб-страниц
books = [] # для сохранения книг

# GET-запрос к серверу
page = requests.get(website)
# Проверка статуса ответа сервера
page.status_code

while url:
    print('\nСкрепинг страницы №', p_count + 1)
    # Отправка GET запроса по URL
    response = requests.get(url)

    # Парсинг HTML страницы с использованием BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    h3_tags = soup.find_all('h3')

    for h3_tag in h3_tags:
        # Поиск тега <a>
        a_tag = h3_tag.find('a', href=True)

        # Создание ссылки на страницу книги
        book_url = website + 'catalogue/' + a_tag['href']

        # Отправка запроса по ссылке на книгу
        book_response = requests.get(book_url)

        # Парсинг страницы книги
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        # экстракция требуемых данных о книге
        title = book_soup.find('h1').text.strip()
        price = float(book_soup.find('p', class_='price_color').text.strip().replace('Â\u00a3', ''))
        stock = int(re.findall(r'\d+', book_soup.find('p', class_='instock availability').text.strip())[0])
        description = book_soup.find('meta', attrs={'name': 'description'})['content']

        book = {
            'Название': title,
            'Цена': price,
            'Наличие': stock,
            'Описание': description
        }

        books.append(book)

        print('Добавили книгу', title, price, stock, description)

    next_button = soup.find('a', string='next')

    # Проверка ссылки на следующую страницу
    if next_button:
        url = website + 'catalogue/' + next_button['href']
        p_count += 1
    else:
        url = None

print("На сайте число книг составляет: ", len(books))

df = pd.DataFrame(books)
print (df)

df.to_json('books.json')

with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, indent=4, ensure_ascii=False)