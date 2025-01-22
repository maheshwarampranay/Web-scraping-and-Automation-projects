from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests

class FillForm:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
    def setup(self):
        self.driver.get("https://docs.google.com/forms/d/e/1FAIpQLSc5u5bNYZYGD6fXIxnwMGXcAyouiwEu6-GNVCQoHSVNjv2VOA/viewform?usp=sharing")
        time.sleep(0.7)
    def fill_details(self, details):
        self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(details[0])
        self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(details[1])
        self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(details[2])
        self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
    def close(self):
        self.driver.quit()

class ScrapeData:
    def __init__(self):
        response = requests.get('https://appbrewery.github.io/Zillow-Clone/')
        soup = BeautifulSoup(response.content, 'html.parser')
        addresses = [i.text.strip() for i in soup.find_all('address')]
        prices = [i.text.strip() for i in soup.find_all(class_ = 'PropertyCardWrapper__StyledPriceLine')]
        links = [i.find('a').get('href') for i in soup.find_all(class_ = 'StyledPropertyCardPhotoBody')]
        self.details = {}
        for i in range(len(addresses)):
            self.details[i] = [addresses[i], prices[i], links[i]]
    def data(self):
        return self.details


data = ScrapeData().data()
filler = FillForm()
for i in data.values():
    filler.setup()
    filler.fill_details(i)
filler.close()