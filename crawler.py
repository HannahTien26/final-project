import os
import re
import requests
import psycopg2
from bs4 import BeautifulSoup

DATABASE_URL = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"

def setup_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ptt_soup (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) UNIQUE,
            question TEXT,
            answer TEXT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def run_crawler():
    
    setup_db()
    
   
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get("https://www.ptt.cc/bbs/TurtleSoup/index.html", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
   
    print("✅ 檢查表格並執行爬蟲成功！")

if __name__ == "__main__":
    run_crawler()