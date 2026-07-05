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
    print("【爬蟲】開始執行抓取任務...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        
        url = "https://nosca395311.pixnet.net/blog/posts/17330712171"
        driver.get(url)
        time.sleep(10)  
        
        
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        results = [p.text for p in paragraphs if len(p.text) > 10]
        
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False)
        print(f"【爬蟲】成功抓取 {len(results)} 筆資料並已存檔。")
        
    except Exception as e:
        print(f"【爬蟲】執行期間發生錯誤: {str(e)}")
    finally:
        driver.quit()

@app.route('/')
def index():
    return "爬蟲機器人運作中..."

@app.route('/data')
def view_data():
    if not os.path.exists('data.json'):
        return "暫無資料，爬蟲可能還在執行中，請稍候再重新整理。"
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return str(data) 

if __name__ == "__main__":
    
    t = threading.Thread(target=run_spider)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=10000)