import  time
from selenium import webdriver
from selenium.webdriver.common.by import By

end_time = time.time() + 180
timeout = time.time() + 5

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie_button = driver.find_element(By.ID, "cookie")

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute('id') for item in items]

while time.time() < end_time:
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text != '':
                cost = int(element_text.split("-")[1].strip().replace(',',''))
                item_prices.append(cost)

        cookie_upgrades = {}
        for i in range(len(item_prices)):
            cookie_upgrades[item_prices[i]] = item_ids[i]

        money_element = driver.find_element(By.ID, value='money').text
        if "," in money_element:
            money_element = money_element.replace(',','')
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id
        try:
            highest_affordable = max(affordable_upgrades)
            driver.find_element(By.ID, value = affordable_upgrades[highest_affordable]).click()
        except:
            pass
        finally:
            timeout = time.time() + 5
    cookie_button.click()
print(driver.find_element(By.ID, "cps").text)
driver.quit()