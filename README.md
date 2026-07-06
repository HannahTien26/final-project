# 海龟汤爬蟲 + 資料庫寫入

負責範圍：從 [limaoqiu.com/haiguitang](https://limaoqiu.com/haiguitang) 爬取全部海龟汤資料，清理格式後寫入 Render 上的 PostgreSQL 資料庫。

## 檔案說明

| 檔案 | 用途 |
|---|---|
| `scraper.py` | 用 Selenium 開啟列表頁，解析頁面內嵌的 JS `data` 陣列，抓出全部 223 筆題目的 id、標題、標籤，再逐篇造訪 `/i/{id}` 存下完整文字，輸出 `haiguitang.json` |
| `split_content.py` | 讀取 `haiguitang.json`，把每篇的文字拆成 `作者` / `汤面` / `汤底` 等欄位，輸出 `haiguitang_clean.json` |
| `insert_data.py` | 讀取 `haiguitang_clean.json`，寫入（或更新）Render PostgreSQL 資料庫裡的 `haiguitang_data` 表格 |
| `requirements.txt` | 需要安裝的套件 |

## 執行步驟

### 1. 進入專案資料夾、啟用虛擬環境
```powershell
cd final-project
.\.venv\Scripts\Activate.ps1
```

### 2. 安裝套件
```bash
pip install -r requirements.txt
```

### 3. 爬取資料
```bash
python scraper.py
```
執行完會產生 `haiguitang.json`（原始爬取內容，每篇一個 `raw_text` 欄位）。

### 4. 清理資料格式
```bash
python split_content.py
```
執行完會產生 `haiguitang_clean.json`（每篇拆好 `author` / `soup_face` / `soup_bottom` 等欄位）。

> 少數幾篇格式比較特殊（沒有明確空行分隔湯面/湯底，或有多重答案版本），拆分結果可能需要人工確認微調，屬正常現象。

### 5. 寫入資料庫
先設定資料庫連線字串（**不要把密碼寫死在程式碼裡**）：
```powershell
$env:DATABASE_URL="postgresql://使用者:密碼@主機/資料庫名稱"
```
再執行：
```bash
python insert_data.py
```
成功會顯示：
```
完成，共寫入/更新 223 筆資料到資料庫。
```

## 資料庫表格結構

`insert_data.py` 會自動建立以下結構的 `haiguitang_data` 表格（如果不存在的話）：

| 欄位 | 型別 | 說明 |
|---|---|---|
| id | SERIAL PRIMARY KEY | 資料庫自動編號 |
| item_id | TEXT UNIQUE | 網站原始題目 id（唯一值，重複執行不會產生重複資料） |
| index_num | INTEGER | 題目在網站上的編號 |
| title | TEXT | 標題 |
| tags | TEXT | 標籤/評分 |
| url | TEXT | 原始題目網址 |
| author | TEXT | 作者（部分題目才有） |
| soup_face | TEXT | 湯面（謎題） |
| soup_bottom | TEXT | 湯底（答案） |

## 注意事項

- `DATABASE_URL` 屬於機密資訊，**不要**寫死在程式碼裡、也不要推上公開的 GitHub repo，一律透過環境變數設定。
- 重複執行 `insert_data.py` 是安全的，會用 `item_id` 判斷更新既有資料，不會產生重複筆數。
