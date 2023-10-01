import json

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from alchemy import create_items, fetch_id


class AvitoParser:
    def __init__(self, url: str, items: list, count=2, version_main=None):
        self.version_main = 116
        self.count = count
        self.items = items
        self.url = url
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument("--headless=new")

        self.driver = uc.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']"):
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.count += 1

    def __parse_page(self):
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in titles:
            item_id = title.get_attribute('data-item-id')
            name = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").text
            description = title.find_element(By.CSS_SELECTOR, "[class='iva-item-descriptionStep-C0ty1']").text
            link = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[data-marker='item-price']").text
            city = link[21:][:link[21:].find('/')]
            price = self.__convert_price(price)
            data = {
                'item_id': item_id,
                'name': name,
                'description': description,
                'link': link,
                'price': price,
                'city': city
            }
            if any([item.lower() in description.lower() for item in self.items]):
                # self.data.append(data)
                new_numbers = []
                if fetch_id(data['item_id']):
                    create_items(data)
                    new_numbers.append(data['item_id'])
                print(new_numbers)

                # self.__printing(data)

            # self.__save_data()

    @staticmethod
    def __convert_price(price):
        '''Преобразовываем цену в цифру'''
        if price == 'Цена не указана':
            print('[!] Цена не указана')
            return 0
        else:
            return int(price[:-1].replace(' ', ''))

    def __printing(self, data):
        print('[+] ITEM_ID = ', data['item_id'])
        print('[+] NAME = ', data['name'])
        print('[+] DECRIPTION = ', data['description'])
        print('[+] LINK = ', data['link'])
        print('[+] PRICE = ', data['price'])
        print('[+] CITY = ', data['city'])

    def __save_data(self):
        with open('items.json', 'w', encoding='UTF-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def run(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()


if __name__ == '__main__':
    AvitoParser(
        url='https://www.avito.ru/voronezh/noutbuki?cd=1&q=lenovo+thinkpad+x1+carbon',
        count=3, version_main=116, items=['Lenovo', 'X1', 'carbon', 'Gen 5', 'Gen 4', 'Gen 6']).run()
