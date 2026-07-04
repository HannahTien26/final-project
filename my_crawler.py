import sys
import os

sys.path.append(os.getcwd())

from models import TurtleSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_spider():
    print("【爬蟲啟動】開始抓取 PTT 海龜湯...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ptt.cc/bbs/TurtleSoup/index.html")
    
    posts = driver.find_elements(By.CLASS_NAME, "r-ent")
    
    for post in posts:
        try:
            title = post.find_element(By.CLASS_NAME, "title").text.strip()
            print(f"成功抓取標題: {title}")
        except Exception as e:
            continue
            
    driver.quit()
    print("【爬蟲結束】任務完成！")

if __name__ == "__main__":
    run_spider()