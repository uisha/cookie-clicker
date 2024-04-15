from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_costs(costs):
    cost_list = []
    for line in costs:
        line = line.text.strip()
        if line == '':
            break

        index = line.find('-')+2
        # print(index)
        cost = line[index:].replace(',', '')
        cost_list.append(int(cost))
    cost_list.reverse()
    return cost_list
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

timer = time.time() + 5*60
buy_time = time.time() + 5

cookie_button = driver.find_element(By.ID, value="cookie")
money = int(driver.find_element(By.ID, value="money").text)
costs = driver.find_elements(By.CSS_SELECTOR, value="#store div b")

while time.time() < timer:
    while time.time() < buy_time:
        cookie_button.click()
    costs = driver.find_elements(By.CSS_SELECTOR, value="#store div b")
    cost_list = get_costs(costs)

    for cost in cost_list:
        money = int(driver.find_element(By.ID, value="money").text.strip(','))
        if cost < money:
            item_index = len(cost_list) - cost_list.index(cost) - 1
            costs[item_index].click()
            break
    buy_time += 5

cookies_per_second = driver.find_element(By.ID, value="cps").text
driver.quit()
print(f"Cookies/Second: {cookies_per_second}")

