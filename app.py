from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # 這行程式碼會自動去抓你剛剛在 Render 設定的 DATABASE_URL
    database_url = os.environ.get('postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k')
    return psycopg2.connect(database_url)

@app.route('/')
def home():
    return "這是我的海龜湯網站首頁！請前往 /api/questions 查看資料。"

@app.route('/api/questions')
def get_questions():
    conn = None
    try:
        # 嘗試連線
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 執行查詢
        cur.execute('SELECT title, raw_text FROM haiguitang_data;') 
        rows = cur.fetchall()
        
        # 關閉 cursor
        cur.close()
        
        # 轉換資料
        data = [{'title': row[0], 'raw_text': row[1]} for row in rows]
        
        # 成功後回傳
        return jsonify(data)
        
    except Exception as e:
        # 發生任何錯誤時，回傳錯誤原因，並且確保連線已關閉
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)