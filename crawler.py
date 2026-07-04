import os
import re
import requests
import psycopg2
from bs4 import BeautifulSoup


DATABASE_URL = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"
PTT_URL = "https://www.ptt.cc/bbs/TurtleSoup/index.html"

def run_crawler():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(PTT_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    titles = soup.find_all('div', class_='title')
    for div in titles:
        a_tag = div.find('a')
        if a_tag:
            title = a_tag.text.strip()
            link = "https://www.ptt.cc" + a_tag['href']
            
            post_res = requests.get(link, headers=headers)
            post_soup = BeautifulSoup(post_res.text, 'html.parser')
            
            main_content = post_soup.find('div', id='main-content')
            if not main_content:
                continue
                
            
            content = main_content.get_text()
            
            
            parts = re.split(r'解答[:：]|湯底[:：]|真相[:：]', content)
            
            question = parts[0].strip()[:500]  # 前半部為湯面
            answer = parts[1].strip() if len(parts) > 1 else "尚無解答"  # 後半部為湯底
            
            sql = "INSERT INTO ptt_soup (title, question, answer) VALUES (%s, %s, %s) ON CONFLICT (title) DO UPDATE SET question = EXCLUDED.question, answer = EXCLUDED.answer"
            cursor.execute(sql, (title, question, answer))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 成功導入新湯，並已自動分開湯面與湯底")

if __name__ == "__main__":
    run_crawler()