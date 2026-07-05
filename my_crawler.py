import json
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return "網站運作中，請訪問 /data 查看題目。"

@app.route('/data')
def view_data():
    try:
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        
        html = "<h1>海龜湯題庫</h1><ul>"
        for item in data:
            html += f"<li>{item}</li>"
        html += "</ul>"
        return html
    except Exception as e:
        return f"讀取資料失敗，請確認是否已先執行 local_spider.py: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)