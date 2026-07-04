import os
import re
import psycopg2
import requests
from bs4 import BeautifulSoup

DATABASE_URL = os.environ.get("DATABASE_URL")

def clean_and_split_ptt_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('div', id='main-content')
    
    if not main_content:
        return "", ""
    
    for meta in main_content.find_all(['div', 'span'], class_=['article-metaline', 'article-metaline-right', 'f2', 'push']):
        meta.extract()
        
    full_text = main_content.get_text()
    
    full_text = re.sub(r'※ 發信站: 批踢踢實業坊\(ptt\.cc\).*', '', full_text)
    full_text = re.sub(r'※ 文章網址:.*', '', full_text)
    full_text = full_text.strip()
    
    split_keywords = [r'解答[：:\s]', r'湯底[：:\s]', r'真相[：:\s]', r'還原[：:\s]']
    pattern = '|'.join(split_keywords)
    
    match = re.search(pattern, full_text)
    
    if match:
        split_index = match.start()
        question = full_text[:split_index].strip()
        answer = full_text[split_index:].strip()
    else:
        question = full_text
        answer = "本題暫無提供解答"
        
    return question, answer

def crawl_ptt_to_db():
    url = "https://www.ptt.cc/bbs/TurtleSoup/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("無法連線到 PTT 海龜湯版")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    articles = soup.find_all('div', class_='r-ent')
    
    for article in articles:
        title_element = article.find('div', class_='title')
        if not title_element or not title_element.find('a'):
            continue
            
        title = title_element.find('a').get_text().strip()
        article_url = "https://www.ptt.cc" + title_element.find('a')['href']
        
        if "刪除" in title:
            continue
            
        detail_res = requests.get(article_url, headers=headers)
        if detail_res.status_code == 200:
            question, answer = clean_and_split_ptt_content(detail_res.text)
            
            try:
                sql = """
                INSERT INTO ptt_soup (title, question, answer) 
                VALUES (%s, %s, %s)
                ON CONFLICT (title) DO NOTHING;
                """
                cursor.execute(sql, (title, question, answer))
                print(f"✅ 成功導入新湯：{title}")
            except Exception as e:
                print(f"寫入資料庫失敗: {e}")
                conn.rollback()
                
    conn.commit()
    cursor.close()
    conn.close()
    print("⏰ 爬蟲任務執行完畢！")

if __name__ == "__main__":
    crawl_ptt_to_db()