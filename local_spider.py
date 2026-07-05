import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://nosca395311.pixnet.net/blog/posts/17330712171")
time.sleep(5)


elements = driver.find_elements(By.TAG_NAME, "p")
data = [e.text.strip() for e in elements if len(e.text.strip()) > 10]


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"成功！已抓取 {len(data)} 段文字到 data.json")
driver.quit()