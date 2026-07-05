import requests
from bs4 import BeautifulSoup
import json

URL = "https://nosca395311.pixnet.net/blog/posts/17330712171"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/149.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

res = requests.get(URL, headers=headers, timeout=15)

print("status:", res.status_code)
print(res.text[:500])

res.raise_for_status()
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, "html.parser")

# 移除無關標籤
for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

# 取得所有文字行
lines = [
    line.strip()
    for line in soup.get_text("\n").splitlines()
    if line.strip()
]

items = []

title = ""
question_lines = []
answer_lines = []
mode = None

for i, line in enumerate(lines):

    # 遇到新題目
    if line.startswith("題目："):

        # 如果前面已有完整題目，先存起來
        if question_lines and answer_lines:
            items.append({
                "title": title,
                "question": "\n".join(question_lines).strip(),
                "answer": "\n".join(answer_lines).strip()
            })

        # 題目前一行當作標題
        title = lines[i - 1].strip() if i > 0 else ""

        question_lines = [
            line.replace("題目：", "", 1).strip()
        ]

        answer_lines = []
        mode = "question"

    # 遇到答案
    elif line.startswith("答案："):

        answer_text = line.replace("答案：", "", 1).strip()

        answer_lines = []

        if answer_text:
            answer_lines.append(answer_text)

        mode = "answer"

    # 一般文字
    else:

        if mode == "question":
            question_lines.append(line)

        elif mode == "answer":
            answer_lines.append(line)

# 儲存最後一題
if question_lines and answer_lines:
    items.append({
        "title": title,
        "question": "\n".join(question_lines).strip(),
        "answer": "\n".join(answer_lines).strip()
    })

# 輸出 JSON
with open("turtle_soup.json", "w", encoding="utf-8") as f:
    json.dump(
        items,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"完成，共抓到 {len(items)} 筆")