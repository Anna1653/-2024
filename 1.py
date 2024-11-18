import requests
import json

endpoints = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города: ")
category = input("Какой вид отдыха ваc интересует (кофейни, музеи, парки и т.д.) : ")
params = {
    "near": city,
    'limit': 10,
    'query': category,
    'fields': 'name,location,rating'
}

headers = {
    "Accept": "application/json",
    "Authorization": "12345"
}

response = requests.get(endpoints, params=params,headers=headers)

print(response.text)

# проверка успешности выполнения запроса
if response.status_code == 200:
    print("Успешный запрос!")
    # вывод текста ответа
    print(response.text)
else:
    print("Запрос не удался с кодом состояния:", response.status_code)

# проверка успешности выполнения запроса
if response.status_code == 201:
    print("Успешный запрос!")
    # вывод текста ответа
    print(response.text)
else:
    print("Запрос не удался с кодом состояния:", response.status_code)

data = response.json()

endpoint = []
for place in data['results']:
    place_name = place.get('name')
    place_address = place.get('location')['formatted_address']
    place_rating = place.get('rating') if 'rating' in place else "Рейтинг не определялся"
    endpoint.append({'name': place_name, 'address': place_address, 'rating': place_rating})

for endpoint in endpoints:
        print(f"Название: {establishment['name']}")
        print(f"Адрес: {establishment['address']}")
        print(f"Рейтинг: {establishment['rating']}")
        print()




