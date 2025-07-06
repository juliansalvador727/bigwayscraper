from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_line_size(store_id):
    url = f"https://gosnappy.io/lineup/?force=true&storeId={store_id}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)

        element = driver.find_element(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'in line')]")
        text = element.text.lower()

        if "no one" in text or "no parties" in text:
            number = 0
        else:
            digits = [word for word in text.split() if word.isdigit()]
            number = int(digits[0]) if digits else None

    except Exception as e:
        print(f"❌ Failed to scrape store {store_id}: {e}")
        number = None

    driver.quit()
    return number