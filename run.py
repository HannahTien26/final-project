import requests
from bs4 import BeautifulSoup
import json
import time

def run_scraper():
    
    session = requests.Session()
    
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    })
    
    
    time.sleep(1) 
    url = "https://www.ptt.cc/bbs/TurtleSoup/index1722.html"
    
    print("正在嘗試建立連線...")
    try:
        
        response = session.get(url, cookies={'over18': '1'}, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='r-ent')
            data = []
            
            for item in items:
                title_tag = item.find('div', class_='title').find('a')
                if title_tag:
                    data.append({
                        "title": title_tag.text.strip(),
                        "url": "https://www.ptt.cc" + title_tag['href']
                    })
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"成功！已產出 data.json，共 {len(data)} 筆資料。")
        else:
            print(f"連線失敗，狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"連線發生錯誤: {e}")

if __name__ == "__main__":
    run_scraper()