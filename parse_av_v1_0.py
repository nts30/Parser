import requests
from bs4 import BeautifulSoup
import time

items = []
years = []
cashes = []
urls = []


class Parser:
    def __init__(self, pages: range):
        self.pages = pages
        self.items = items
        self.years = years
        self.cashes = cashes
        self.urls = urls

        self._get_html()

    def _get_html(self):
        for page in self.pages:
            if page == 1:
                url = 'https://cars.av.by/filter'
            else:
                url = f'https://cars.av.by/filter?page={page}'

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }

            response = requests.get(url, headers=headers)

            try:
                assert response.status_code == 200
                html_source = response.text
                self._get_info(html_source)
            except Exception as ex:
                print(f'[ERROR] {repr(ex)}')
                print(response.status_code)

    def _get_info(self, html_source):
        pages_info = BeautifulSoup(html_source, 'html.parser')

        car_names = pages_info.find_all('a', class_='listing-item__link')
        for name in car_names:
            self.items.append(name.text)
            self.urls.append(f'https://cars.av.by{name["href"]}')

        items_cashes = pages_info.find_all('div', class_='listing-item__priceusd')
        for cash in items_cashes:
            self.cashes.append(cash.text)

        years_list = pages_info.find_all('div', class_='listing-item__params')
        for year in years_list:
            self.years.append(year.text)


if __name__ == "__main__":
    start_time = time.time()

    parse = Parser(range(1, 2000))
    all_info = list(zip(items, years, cashes, urls))

    for i in all_info:
        print(f'Марка: {i[0]}, Год: {i[1]}, Цена: {i[2]}, Ссылка: {i[-1]}')

    print(len(all_info))
    end_time = time.time()
    print(f'Время выполнения программы: {end_time - start_time}')
