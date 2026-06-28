from flask import Flask, render_template, request
import random
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def load_soups_from_html():
    soups = []
    # 這裡確保檔案名稱跟你同學的一樣
    file_path = "my_source.html" 
    
    if not os.path.exists(file_path):
        print(f"找不到 {file_path} 檔案喔！請確認它跟 app.py 放在同一個資料夾。")
        return soups

    # 讀取同學做好的 HTML 檔案
    with open(file_path, "r", encoding="utf-8") as f:
        soup_doc = BeautifulSoup(f, "html.parser")

    # 抓出所有 class 為 soup-item 的區塊
    items = soup_doc.find_all("div", class_="soup-item")
    
    for item in items:
        # 抓取標題、湯麵、湯底
        title_element = item.find("h2", class_="soup-title")
        question_element = item.find("p", class_="soup-question")
        answer_element = item.find("p", class_="soup-answer")
        
        # 確保資料都有抓到才放進去
        if title_element and question_element and answer_element:
            title = title_element.text.strip()
            question = question_element.text.strip()
            answer = answer_element.text.strip()
            
            # 自動判斷分類（1-15題恐怖，16-30題搞笑，31-45題感人）
            try:
                num = int(title.split(".")[0])
                if num <= 15:
                    tag = "恐怖"
                elif num <= 30:
                    tag = "搞笑"
                else:
                    tag = "感人"
            except:
                tag = "全部" # 萬一標題沒有數字，就丟到「全部」

            soups.append({
                "tag": tag,
                "title": title,
                "content": question,
                "answer": answer
            })
        
    return soups

@app.route("/")
def home():
    all_soups = load_soups_from_html()
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
    all_soups = load_soups_from_html()
    
    if all_soups:
        lucky_soup = random.choice(all_soups)
        return render_template("index.html", soups=[lucky_soup], current_category="隨機")
    else:
        return "題庫還沒準備好喔！"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)