import os
import json
import time
import threading
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)

def run_spider():
    print("【爬蟲】啟動中...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        url = "https://nosca395311.pixnet.net/blog/posts/17330712171"
        driver.get(url)
        time.sleep(20)  
        
        
        content = driver.find_element(By.TAG_NAME, "body").text
        
        
        data = [content] 
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            
        print("【爬蟲】任務完成，內容已寫入 data.json。")
    except Exception as e:
        print(f"【爬蟲】發生錯誤: {e}")
    finally:
        driver.quit()

@app.route('/')
def index():
    return "系統運作中，請訪問 /data 查看結果。"

@app.route('/data')
def view_data():
    if not os.path.exists('data.json'):
        return "資料抓取中，請稍候..."
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return str(data)

if __name__ == "__main__":
    threading.Thread(target=run_spider, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)