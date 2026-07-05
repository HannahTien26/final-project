import psycopg2

DATABASE_URL = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # 建立表格（確保它存在）
    cur.execute('''
        CREATE TABLE IF NOT EXISTS haiguitang_data (
            id SERIAL PRIMARY KEY,
            title TEXT,
            raw_text TEXT
        )
    ''')
    
    # 寫入一則資料
    cur.execute("INSERT INTO haiguitang_data (title, raw_text) VALUES (%s, %s)", 
                ("測試題目：小明為什麼會死？", "小明在沙漠中拿著一根火柴。"))
    
    conn.commit() # 重要：一定要這行才會存進去
    print("--- 資料寫入成功！ ---")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"--- 發生錯誤: {e} ---")