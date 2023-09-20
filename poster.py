import json
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class AvitoPoster:
    def __init__(self, url: str, version_main=None):
        self.version_main = version_main
        # self.count = count
        # self.items = items
        self.url = url
        self.data = []

    def __set_up(self):
        # options = Options()
        # options.add_argument("--headless=new")

        self.driver = uc.Chrome(version_main=self.version_main)
        # self.driver = uc.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)
        time.sleep(5)

    def create_item(self):
        self.driver.find_element(By.CSS_SELECTOR, "[data-marker='header/login-button']").click()
        time.sleep(5)



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
            if any([item.lower() in description.lower() for item in self.items]):
                self.data.append(data)
                print(name, description, link, price)

        self.__save_data()

    def __save_data(self):
        with open('items.json', 'w', encoding='UTF-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def run(self):
        self.__set_up()
        self.__get_url()
        self.create_item()
        # self.__paginator()


if __name__ == '__main__':
    url = 'https://www.avito.ru/'
    AvitoPoster(url=url,
                version_main=116).run()
