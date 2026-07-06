"""
後處理腳本：讀取 scraper.py 產生的 haiguitang.json，
把每一筆的 raw_text 拆成 作者 / 汤面 / 汤底 等乾淨欄位，
存成新的 haiguitang_clean.json

使用方式：
    python split_content.py
"""

import json
import re

INPUT_FILE = "haiguitang.json"
OUTPUT_FILE = "haiguitang_clean.json"


def split_one(item):
    text = item.get("raw_text", "")

    # 去掉開頭 "海龟汤：{标题}\n"
    text = re.sub(r"^海龟汤：.*?\n", "", text, count=1)

    # 去掉結尾的導覽列文字（從第一次出现 "猫球博客" 开始都是导览列）
    nav_pos = text.find("猫球博客")
    if nav_pos != -1:
        text = text[:nav_pos]

    text = text.strip("\n").strip()

    # 如果开头有 "作者：xxx" 这一行，取出来单独存
    author = ""
    author_match = re.match(r"作者[：:]\s*(.+)", text)
    if author_match:
        author = author_match.group(1).strip()
        # 把這一行從內文移除
        text = text[author_match.end():].lstrip("\n").strip()

    # 用空行（\n\n 或以上）分割出段落，最後一段當作汤底，前面全部当汤面
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

    if len(paragraphs) >= 2:
        soup_face = "\n".join(paragraphs[:-1])
        soup_bottom = paragraphs[-1]
    elif len(paragraphs) == 1:
        soup_face = paragraphs[0]
        soup_bottom = ""
    else:
        soup_face = ""
        soup_bottom = ""

    return {
        "index": item.get("index"),
        "id": item.get("id"),
        "title": item.get("title"),
        "tags": item.get("tags"),
        "url": item.get("url"),
        "author": author,
        "soup_face": soup_face,      # 汤面
        "soup_bottom": soup_bottom,  # 汤底
    }


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    cleaned = [split_one(item) for item in items]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"處理完成，共 {len(cleaned)} 筆，已存到 {OUTPUT_FILE}")
    print("建議打開檢查幾筆，看汤面/汤底有沒有拆對（少數篇目排版可能不同，需要手動微調）")


if __name__ == "__main__":
    main()
