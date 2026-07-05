"""
把 https://limaoqiu.com/haiguitang 的完整 HTML 存成 page_source.html
執行完後，把同資料夾產生的 page_source.html 這個檔案直接拖進聊天視窗給我
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LIST_URL = "https://limaoqiu.com/haiguitang"


def main():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get(LIST_URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/i/']"))
    )
    time.sleep(3)  # 給 JS 多一點時間跑完

    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("已存檔：page_source.html")
    print("請把這個檔案直接拖進聊天視窗給 Claude 看")

    driver.quit()


if __name__ == "__main__":
    main()
