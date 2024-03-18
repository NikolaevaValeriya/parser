import subprocess
import sys
import os

def install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Вызов функции для установки зависимостей
install_requirements()

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
import pandas as pd

cities = ['Сидней', 'Канберра', 'Бирмингем', 'Лондон', 'Буэнос-Айрес', 'Мендоса', 'Гюмри', 'Берлин',
          'Мюнхен', 'Афины', 'Родос', 'Батуми', 'Тбилиси', 'Хургада', 'Каир', 'Мадрид', 'Барселона',
          'Рим', 'Венеция', 'Астана', 'Алма-Ата', 'Ванкувер', 'Оттава', 'Кирения', 'Никосия', 'Гейрангер',
          'Осло', 'Абу-Даби', 'Дубай', 'Нью-Йорк', 'Лос-Анджелес', 'Пхукет', 'Бангкок', 'Аланья', 'Сиде',
          'Париж', 'Марсель', 'Будва', 'Улцинь', 'Прага', 'Карловы Вары', 'Стокгольм', 'Кируна', 'Канди',
          'Велигаме', 'Сеул', 'Пусан', 'Токио', 'Наре']


cities_urls = []

cities_g = {
    'Ереван': 293932, 'Сидней':	255060, 'Канберра':	255057, 'Бирмингем': 186402, 'Лондон': 186338,
    'Буэнос-Айрес': 312741, 'Мендоса': 312781, 'Гюмри': 815353, 'Берлин': 187323, 'Мюнхен': 187309,
    'Афины': 189400, 'Родос': 635613, 'Батуми': 297576, 'Тбилиси': 294195, 'Хургада': 297549,
    'Каир': 294201, 'Мадрид': 187514, 'Барселона': 187497, 'Рим': 187791, 'Венеция': 187870,
    'Астана': 293944, 'Алма-Ата': 298251, 'Ванкувер': 154943, 'Оттава': 155004, 'Кирения': 190378,
    'Никосия': 190383, 'Гейрангер': 642196, 'Осло': 190479, 'Абу-Даби': 294013, 'Дубай': 295424,
    'Нью-Йорк':	60763, 'Лос-Анджелес': 32655, 'Пхукет': 293920, 'Бангкок': 293916, 'Аланья': 297961,
    'Сиде': 297968, 'Париж': 187147, 'Марсель': 187253, 'Будва': 304074, 'Улцинь': 652061, 'Прага': 274707,
    'Карловы Вары': 274697, 'Стокгольм': 189852, 'Кируна': 189815, 'Канди': 304138, 'Велигаме': 612380,
    'Сеул': 294197, 'Пусан': 297884, 'Токио': 298184, 'Нара': 298198
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'DNT': '1',
    'Pragma': 'no-cache',
}

if os.path.exists('data.csv'):
    data = pd.read_csv('data.csv')
else:
    data = pd.DataFrame(columns=['hotel', 'city', 'url', 'price', 'rating', 'stars', 'price_range', 'lowest_price', 'highest_price'])
# START PARSING

for g in tqdm(cities_g):
    hotels = []
    oa_number = 0
    oa_stop = None
    flag_stop = False

    while True:
        try:
            g_iter = str(cities_g[g])
            oa_iter = str(oa_number)
            url = 'https://www.tripadvisor.ru/Hotels-g' + g_iter + '-oa' + oa_iter

            for _ in range(15):
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    break
                
            if response.status_code != 200:
                print(f'url {url} не нашелся ')


            soup = BeautifulSoup(response.text, 'html')
            name = soup.find_all('a', class_ = 'BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS')
            
            if oa_stop is None:
                oa_stop = int(soup.find('span', class_ = 'b').text.replace('\xa0', '').split(' ')[0])
            

            
            stop_count = 0

            for i in name:
                
                if data['url'].str.contains(i['href']).any():
                    print(f'Такой отель уже есть, url = {i["href"]}')
                    continue

                hotel = i.find('h3')

                if hotel != None:
                    hotel = hotel.text.split('. ')
                    

                    if hotel[1] not in hotels:

                        hotels.append(hotel[1])

                        print(hotel[1])

                        url2 = 'https://www.tripadvisor.ru' + str(i['href'])
                        for _ in range(15):
                            response2 = requests.get(url2, headers=headers)
                            if response2.status_code == 200:
                                break
                        soup2 = BeautifulSoup(response2.text, 'html')

                        price = soup2.find('div', class_ = 'biGQs _P fiohW uuBRH')
                        if price != None:
                            price = price.text
                            print(price)
                        else:
                            price = np.nan

                        rating = soup2.find('span', class_ = 'kJyXc P')
                        if rating != None:
                            rating = rating.text
                        else:
                            rating = np.nan

                        s = soup2.find('svg', class_ = 'JXZuC d H0')
                        if s != None:
                            stars = s.find('title').text.split(' ')[0]
                        else:
                            stars = np.nan

                        price_range = soup2.find('div', class_ = 'IhqAp Ci')

                        if price_range != None:
                            price_range = price_range.text.split(' (')[0]
                            lowest_price = price_range.split(' - ')[0]
                            highest_price = price_range.split(' - ')[1]
                        else:
                            price_range = np.nan
                            lowest_price = np.nan
                            highest_price = np.nan


                        hotel_info = pd.DataFrame(
                            {
                                'hotel': hotel[1],
                                'city': g,
                                'url': url2,
                                'price': price,
                                'rating': rating,
                                'stars': stars,
                                'price_range': price_range,
                                'lowest_price': lowest_price,
                                'highest_price': highest_price
                            }, index=[0]
                        )


                        data = pd.concat([data, hotel_info])

                        data.to_csv('data.csv', index=False)

                        print(hotel[1])

                    
                    else:
                        stop_count += 1 
                        print(f'{stop_count} повторов отелей на странице')

                        if stop_count > 8:
                            flag_stop = True
                            print(f'flag_stop = True')
                            break

                        continue

                else:
                    # print(f'Hotel is None, url = {url}')
                    continue
            
            if flag_stop:
                print('While остановился из-за повторов')
                break

            if oa_number > oa_stop:
                print('While остановился из-за oa_number > oa_stop')
                break

            oa_number += 30        


        except Exception as e:
            if flag_stop:
                break
            print(f' Исключение {e}')
            oa_number += 30
            continue
