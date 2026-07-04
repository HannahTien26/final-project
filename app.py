from flask import Flask, render_template, request
import random
import os
import psycopg2 

app = Flask(__name__)

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL', 'postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k')
    return psycopg2.connect(db_url)

def load_soups_from_db():
    soups = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT title, content, answer FROM turtle-soup-db;')
        rows = cur.fetchall()
        
        cur.close()
        conn.close()

        for row in rows:
            title = row[0]
            question = row[1]
            answer = row[2]
            
            try:
                num = int(title.split(".")[0])
                if num <= 15:
                    tag = "恐怖"
                elif num <= 30:
                    tag = "搞笑"
                else:
                    tag = "感人"
            except:
                tag = "全部" 

            soups.append({
                "tag": tag,
                "title": title,
                "content": question,
                "answer": answer
            })
    except Exception as e:
        print(f"資料庫連線或讀取失敗啦！錯誤訊息：{e}")
        
    return soups

@app.route("/")
def home():
    all_soups = load_soups_from_db()
    selected_category = request.args.get("category")
    
    if selected_category:
        filtered_soups = [soup for soup in all_soups if soup.get("tag") == selected_category]
    else:
        filtered_soups = all_soups
        
    return render_template(
        "index.html", 
        soups=filtered_soups, 
        current_category=selected_category
    )

@app.route("/random")
def random_soup():
    all_soups = load_soups_from_db()
    
    if all_soups:
        lucky_soup = random.choice(all_soups)
        return render_template("index.html", soups=[lucky_soup], current_category="隨機")
    else:
        return "題庫還沒準備好喔！請確認資料庫有連上且有資料。"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)