import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(
#    r"D:\scrapercourse-shopeemall\scrapercourse-shopeemall\chromedriver.exe")
# driver.get("https://www.google.com")
for page in range(1, 3):
    driver.get(
        f'https://shopee.tw/mall/%E5%B1%85%E5%AE%B6%E7%94%9F%E6%B4%BB-cat.11040925/popular?pageNumber={page}')

    # driver.get(
    #    'https://shopee.tw/mall/%E5%B1%85%E5%AE%B6%E7%94%9F%E6%B4%BB-cat.11040925')
    # time.sleep(5)

    ActionChains(driver).move_by_offset(100, 100).click().perform()

    locator = (By.CSS_SELECTOR,
               "div[class='col-xs-2 recommend-products-by-view__item-card-wrapper']")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(locator),
        "找不到指定的元素"
    )

    cards = driver.find_elements(
        By.CSS_SELECTOR, "div[class='col-xs-2 recommend-products-by-view__item-card-wrapper']")

    items = []

    for card in cards:
        # ActionChains(driver).move_to_element(card).perform()
        title = card.find_element(
            By.CSS_SELECTOR, "div[class='ie3A+n bM+7UW Cve6sh']").text
        price = card.find_element(
            By.CSS_SELECTOR, "div[class='vioxXd rVLWG6']").text
        link = card.find_element(
            By.TAG_NAME, "a").get_attribute('href')
        items.append((title, price, link))
    # print(items)

    result = []
    for item in items:
        driver.get(item[2])

        for i in range(8):
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)

        comments = driver.find_elements(By.CSS_SELECTOR, "div[class='Em3Qhp']")
        for comment in comments:
            result.append((item[0], item[1], comment.text))
        break
    print(f"第{page}頁")
    print(result)
