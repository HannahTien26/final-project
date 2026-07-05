import requests
from bs4 import BeautifulSoup
import json
import time

def get_content(url):
    try:
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, cookies={'over18': '1'}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        main_content = soup.find('div', id='main-content')
        if not main_content:
            return "無法解析內文"
        
        
        for tag in main_content.select('div.push, div.article-metaline, div.article-metaline-right'):
            tag.decompose()
            
        return main_content.text.strip()
    except Exception as e:
        return f"錯誤: {str(e)}"

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


print(f"準備抓取 {len(data)} 篇文章的內容...")
for item in data:
    if 'url' in item:
        print(f"正在抓取: {item['title']}")
        item['content'] = get_content(item['url'])
        time.sleep(1) 


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("深度抓取完成！現在 data.json 裡應該有完整內容了。")