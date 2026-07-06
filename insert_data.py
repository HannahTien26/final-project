"""
把 haiguitang_clean.json 裡的資料寫進 Render PostgreSQL 資料庫

使用方式：
    在終端機先設定環境變數（不要把密碼直接寫在程式碼裡）：

    Windows PowerShell:
        $env:DATABASE_URL="postgresql://soup_admin:你的密碼@dpg-xxxx.singapore-postgres.render.com/soup_db_2l2k"

    然後執行：
        python insert_data.py
"""

import json
import os

import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
DATA_FILE = "haiguitang_clean.json"


def main():
    if not DATABASE_URL:
        print("錯誤：找不到環境變數 DATABASE_URL，請先設定好再執行。")
        print('例如 PowerShell：$env:DATABASE_URL="你的資料庫連線字串"')
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # 建立表格（如果還不存在），欄位對應 haiguitang_clean.json 的結構
    cur.execute("""
        CREATE TABLE IF NOT EXISTS haiguitang_data (
            id SERIAL PRIMARY KEY,
            item_id TEXT UNIQUE,
            index_num INTEGER,
            title TEXT,
            tags TEXT,
            url TEXT,
            author TEXT,
            soup_face TEXT,
            soup_bottom TEXT
        )
    """)

    inserted = 0
    for item in items:
        cur.execute("""
            INSERT INTO haiguitang_data
                (item_id, index_num, title, tags, url, author, soup_face, soup_bottom)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (item_id) DO UPDATE SET
                index_num = EXCLUDED.index_num,
                title = EXCLUDED.title,
                tags = EXCLUDED.tags,
                url = EXCLUDED.url,
                author = EXCLUDED.author,
                soup_face = EXCLUDED.soup_face,
                soup_bottom = EXCLUDED.soup_bottom
        """, (
            item.get("id"),
            item.get("index"),
            item.get("title"),
            item.get("tags"),
            item.get("url"),
            item.get("author"),
            item.get("soup_face"),
            item.get("soup_bottom"),
        ))
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"完成，共寫入/更新 {inserted} 筆資料到資料庫。")


if __name__ == "__main__":
    main()
