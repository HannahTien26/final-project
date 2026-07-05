import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    # 這是正確的用法：去抓取環境變數中名為 'DATABASE_URL' 的值
    database_url = os.environ.get('DATABASE_URL')
    
    # 如果 DATABASE_URL 沒有設定，這裡會報錯提醒你
    if not database_url:
        raise Exception("請在 Render 的 Environment 中設定 DATABASE_URL 變數")
        
    return psycopg2.connect(database_url)

@app.route('/')
def home():
    return "這是我的海龜湯網站首頁！請前往 /api/questions 查看資料。"

@app.route('/api/questions')
def get_questions():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 執行查詢
        cur.execute('SELECT title, raw_text FROM haiguitang_data;') 
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # 轉換資料
        data = [{'title': row[0], 'raw_text': row[1]} for row in rows]
        return jsonify(data)
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 雲端上 Render 會自動透過 Gunicorn 啟動，這裡的 debug=True 只在本地測試用
    app.run()