from flask import Flask, render_template, request
import random

app = Flask(__name__)

def load_soups_from_txt():
    soups = []
    current_soup = {}
    current_category = "全部" 
    
    with open("data/soups.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            
            if not line:
                continue
                
            if "恐怖篇" in line:
                current_category = "恐怖"
                continue
            elif "搞笑篇" in line:
                current_category = "搞笑"
                continue
            elif "感人篇" in line:
                current_category = "感人"
                continue
                
        
            if line[0].isdigit() and "." in line:
                if current_soup:
                    soups.append(current_soup)
                    current_soup = {} 
                
                current_soup["tag"] = current_category
                
                title_parts = line.split(".", 1)
                if len(title_parts) > 1:
                    current_soup["title"] = title_parts[1].strip()
                    
            elif line.startswith("湯麵："):
                current_soup["content"] = line.replace("湯麵：", "").strip()
                
            elif line.startswith("湯底：") or line.startswith("湯對："):
                text = line.replace("湯底：", "").replace("湯對：", "").strip()
                current_soup["answer"] = text
                
        if current_soup:
            soups.append(current_soup)
            
    return soups

@app.route("/")
def home():
    all_soups = load_soups_from_txt()
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
    all_soups = load_soups_from_txt()
    
    if all_soups:
        lucky_soup = random.choice(all_soups)
        return render_template("index.html", soups=[lucky_soup], current_category="隨機")
    else:
        return "題庫還沒準備好喔！"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)