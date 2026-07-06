import psycopg2

DB_URL = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # 這次我們不限制數量，把所有 id 和標題都抓出來，並按照 id 排序
    cur.execute("SELECT id, title FROM turtle_soups ORDER BY id;")
    rows = cur.fetchall()
    
    print(f"\n📊 掃描完畢！資料庫裡總共有 【 {len(rows)} 】 筆資料\n" + "="*50)
    
    for row in rows:
        print(f"ID: {row[0]:<4} | 標題: {row[1]}")
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ 連線失敗，原因：{e}")