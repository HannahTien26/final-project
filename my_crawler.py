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
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        
        driver.get("https://nosca395311.pixnet.net/blog/posts/17330712171")
        time.sleep(15)  
        
       
        elements = driver.find_elements(By.TAG_NAME, "p")
        
        data = [el.text for el in elements if len(el.text) > 5]
        
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            
        print(f"【爬蟲】成功抓取 {len(data)} 筆內容。")
    except Exception as e:
        print(f"【爬蟲】失敗: {e}")
    finally:
        driver.quit()

@app.route('/')
def index():
    return "爬蟲服務運作中，請訪問 /data 查看結果。"

@app.route('/data')
def view_data():
    if not os.path.exists('data.json'):
        return "資料抓取中，請稍候重新整理頁面..."
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return str(data)

if __name__ == "__main__":
    
    threading.Thread(target=run_spider, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)