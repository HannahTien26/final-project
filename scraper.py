"""
最小 Selenium 爬蟲：抓取 limaoqiu.com/haiguitang 的海龜湯列表 + 各篇內容

重要發現：
這個網站的「翻页：1-49 50-99...」只是捲動用的錨點，不是真正的分頁機制。
所有題目的標題／標籤／評分／ID，其實已經寫在列表頁原始碼裡一段 JS 的
`data` 陣列中（每一筆長得像："204. 兄弟 <small>★★★</small>／3689615／／"）。
所以完全不需要模擬點擊，只要抓下列表頁原始碼、用文字解析就能拿到全部筆數。
"""

import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LIST_URL = "https://limaoqiu.com/haiguitang"
OUTPUT_FILE = "haiguitang.json"


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1600")
    return webdriver.Chrome(options=options)


def parse_list(page_source):
    """從列表頁原始碼裡解析出 JS 的 data 陣列，回傳 [{id, index, title, tags}, ...]"""
    m = re.search(r"let data = new Array\((.*?)\);", page_source, re.S)
    if not m:
        raise RuntimeError("找不到 data 陣列，網站結構可能已經改變")

    raw_block = m.group(1)
    raw_items = re.findall(r'"((?:\\.|[^"\\])*)"', raw_block)

    items = []
    for raw in raw_items:
        parts = raw.split("／")
        if len(parts) < 2:
            continue
        title_html, item_id = parts[0], parts[1]
        if not item_id.isdigit():
            continue

        tag_match = re.search(r"<small[^>]*>(.*?)</small>", title_html)
        tags = tag_match.group(1).strip() if tag_match else ""
        title = re.sub(r"<[^>]+>", "", title_html).strip()
        idx_match = re.match(r"(\d+)\.\s*(.*)", title)
        index = int(idx_match.group(1)) if idx_match else None
        title = idx_match.group(2).strip() if idx_match else title

        items.append({"index": index, "id": item_id, "title": title, "tags": tags})

    return items


def scrape_item(driver, item_id):
    """打開單一海龜湯頁面 /i/{id}，回傳整頁文字內容"""
    url = f"https://limaoqiu.com/i/{item_id}"
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    text = driver.find_element(By.TAG_NAME, "body").text.strip()
    return {"url": url, "raw_text": text}


def main():
    driver = get_driver()
    try:
        print("正在載入列表頁...")
        driver.get(LIST_URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/i/']"))
        )
        time.sleep(1)

        items = parse_list(driver.page_source)
        print(f"共解析到 {len(items)} 筆海龜湯（預期 249）")

        results = []
        for i, item in enumerate(items, 1):
            try:
                detail = scrape_item(driver, item["id"])
                merged = {**item, **detail}
                results.append(merged)
                print(f"[{i}/{len(items)}] 已抓取 id={item['id']}《{item['title']}》")
            except Exception as e:
                print(f"抓取失敗 id={item['id']}: {e}")
            time.sleep(0.5)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"完成，共存 {len(results)} 筆到 {OUTPUT_FILE}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()