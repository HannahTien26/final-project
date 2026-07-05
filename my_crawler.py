from flask import Flask
import threading
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


def get_text_or_none(driver, by, value):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        return element.text.strip()
    except Exception as e:
        print(f"警告: 無法找到元素 {value} - {e}")
        return None

def run_spider():
    print("【爬蟲】啟動中，準備連線...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    
    target_url = "https://nosca395311.pixnet.net/blog/posts/17330712171"
    
    try:
        print(f"【爬蟲】正在訪問網頁: {target_url}")
        driver.get(target_url)
        
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "article-content"))
        )
        
        print("【爬蟲】網頁載入完成，開始分析內容...")
        
        
        article_body = driver.find_element(By.CLASS_NAME, "article-content")
        
       
        paragraphs = article_body.find_elements(By.TAG_NAME, "p")
        
        title = driver.title
        surface = "尚未抓取到湯面"
        bottom = "尚未抓取到湯底"

        
        for p in paragraphs:
            text = p.text.strip()
            if "湯面" in text and "：" in text:
                surface = text.replace("湯面：", "").replace("湯面:", "")
            elif "湯底" in text and "：" in text:
                bottom = text.replace("湯底：", "").replace("湯底:", "")
        
        print("【爬蟲】抓取結果:")
        print(f"  標題: {title}")
        print(f"  湯面: {surface}")
        print(f"  湯底: {bottom}")

       
        scraped_data = {
            "title": title,
            "surface": surface,
            "bottom": bottom,
            "url": target_url,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        
        if not os.path.exists('/app'):
            os.makedirs('/app')
            
        with open('/app/data.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False)
        
        print("【爬蟲】資料已成功儲存至 /app/data.json")

    except Exception as e:
        print(f"【爬蟲】發生錯誤: {e}")
        
    finally:
        driver.quit()
        print("【爬蟲】瀏覽器已關閉，任務結束")

@app.route('/')
def index():
    return "爬蟲機器人運作中，正在監控海龜湯... (最新狀態: 已執行抓取)"


@app.route('/data')
def view_data():
    try:
        with open('/app/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"error": "目前還沒有爬蟲資料，請稍候或檢查 Logs"}

if __name__ == "__main__":
    
    spider_thread = threading.Thread(target=run_spider)
    spider_thread.daemon = True
    spider_thread.start()
    
    
    app.run(host='0.0.0.0', port=10000)