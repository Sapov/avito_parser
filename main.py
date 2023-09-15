import json

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class AvitoParser:
    def __init__(self, url: str, items: list, count=100, version_main=None):
        self.version_main = version_main
        self.count = count
        self.items = items
        self.url = url
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument("--headless=new")

        self.driver = uc.Chrome(version_main=self.version_main, options=options)
        # self.driver = uc.Chrome(version_main=116)

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
            name = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").text
            description = title.find_element(By.CSS_SELECTOR, "[class='iva-item-descriptionStep-C0ty1']").text
            link = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[data-marker='item-price']").text
            data = {
                'name': name,
                'description': description,
                'link': link,
                'price': price
            }
            self.data.append(data)
            print(name, description, link, price)
        self.__save_data()

    def __save_data(self):
        with open('items.json', 'w', encoding='UTF-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def run(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()


if __name__ == '__main__':
    AvitoParser(
        url='https://www.avito.ru/voronezh?cd=1&q=%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D1%8C+%D0%BD%D0%B0+%D0%B1%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%D0%B5',
        count=3, version_main=116, items=['печать', 'баннер']).run()
