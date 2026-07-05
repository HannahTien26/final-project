import psycopg2

DATABASE_URL = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 刪除舊表 (防止殘留錯誤)，並建立新表
cur.execute("DROP TABLE IF EXISTS haiguitang_data;")
cur.execute('''
    CREATE TABLE haiguitang_data (
        id SERIAL PRIMARY KEY,
        title TEXT,
        raw_text TEXT
    );
''')

conn.commit()
cur.close()
conn.close()
print("表格 'haiguitang_data' 建立成功！")