import sys
import os
import time
import threading
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)


@app.route("/")
def home():
    return "爬蟲機器人運作中，正在監控海龜湯..."

def run_spider():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    while True:
        try:
            print("【自動爬蟲啟動】連線至 Pixnet...")
            driver = webdriver.Chrome(options=options)
            driver.get("https://nosca395311.pixnet.net/blog/posts/17330712171")
            
            
            time.sleep(5)
            
            
            title = driver.find_element(By.TAG_NAME, "h1").text.strip()
            
            
            content = driver.find_element(By.CLASS_NAME, "article-content-inner").text.strip()
            
            
            if "湯底" in content:
                parts = content.split("湯底", 1)
                surface = parts[0].replace("湯面", "").strip()
                bottom = parts[1].strip()
                
                print(f"【成功抓取】標題: {title}")
                print(f"【湯面】: {surface[:50]}...")
                print(f"【湯底】: {bottom[:50]}...")
            else:
                print("【警告】找不到『湯底』關鍵字，無法切割")
            
            driver.quit()
            print("【完成】休息 1 小時後再次爬取...")
            time.sleep(3600)
            
        except Exception as e:
            print(f"發生錯誤: {e}")
            time.sleep(300)

if __name__ == "__main__":
    
    thread = threading.Thread(target=run_spider)
    thread.daemon = True
    thread.start()
    
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))