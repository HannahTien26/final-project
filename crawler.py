import os
import requests
import psycopg2
from bs4 import BeautifulSoup

DATABASE_URL = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"
PTT_URL = "https://www.ptt.cc/bbs/TurtleSoup/index.html"

def run_crawler():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(PTT_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    titles = soup.find_all('div', class_='title')
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    for div in titles:
        a_tag = div.find('a')
        if a_tag:
            title = a_tag.text.strip()
           
            sql = "INSERT INTO ptt_soup (title, question, answer) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
            cursor.execute(sql, (title, "待更新", "待更新"))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 成功導入新湯")

if __name__ == "__main__":
    run_crawler()