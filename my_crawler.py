import os
import json
import time
import threading
from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)


def run_spider():
    print("【爬蟲】啟動中...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://nosca395311.pixnet.net/blog/posts/17330712171"
        driver.get(url)
        time.sleep(5)  

        
        content_box = driver.find_element(By.CLASS_NAME, "article-content")
        paragraphs = content_box.find_elements(By.TAG_NAME, "p")
        
        questions = []
        for p in paragraphs:
            text = p.text.strip()
            
            if len(text) > 5 and ("." in text[:3] or "：" in text):
                questions.append(text)
        
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False)
            
        print(f"【爬蟲】成功抓取 {len(questions)} 筆資料")
    except Exception as e:
        print(f"【爬蟲】發生錯誤: {e}")
    finally:
        driver.quit()


@app.route('/')
def index():
    return "爬蟲機器人運作中，請訪問 /data 查看已抓取的題目。"

@app.route('/data')
def view_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        
        html = "<h1>海龜湯題目列表</h1><ul>"
        for item in data:
            html += f"<li>{item}</li>"
        html += "</ul>"
        return html
    return "暫無資料，爬蟲執行中..."

if __name__ == "__main__":
   
    spider_thread = threading.Thread(target=run_spider)
    spider_thread.daemon = True
    spider_thread.start()
    
    app.run(host='0.0.0.0', port=10000)