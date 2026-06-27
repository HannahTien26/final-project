import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import json

async def scrape_soup():
    async with async_playwright() as p:
        # GitHub Actions 必須用 headless=True (不顯示瀏覽器畫面)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. 前往海龜湯網站（請換成你的目標網址）
        print("正在載入海龜湯網頁...")
        await page.goto('https://example-turtle-soup-site.com/latest') 
        
        # 2. 處理動態載入：等待題目列表出現
        await page.wait_for_selector('.soup-card')
        
        soup_list = []
        
        # 抓取前 10 個海龜湯
        cards = await page.locator('.soup-card').all()
        for i, card in enumerate(cards[:10]):
            # 抓取題目標題與湯面（內容）
            title = await card.locator('.soup-title').inner_text()
            question = await card.locator('.soup-content').inner_text()
            
            # 🔥 動態操作關鍵：點擊「觀看湯底」按鈕，讓答案載入
            answer_button = card.locator('.show-answer-btn')
            if await answer_button.is_visible():
                await answer_button.click()
                # 等待 1 秒讓答案動態跑出來
                await page.wait_for_timeout(1000) 
            
            # 抓取跑出來的湯底（答案）
            answer = await card.locator('.soup-answer').inner_text()
            
            soup_list.append({
                'id': i + 1,
                'title': title,
                'question': question,
                'answer': answer
            })
            print(f"成功抓取第 {i+1} 碗湯：{title}")
            
        # 3. 儲存成 JSON 檔案（海龜湯有題目有答案，用 JSON 存比 CSV 更好結構化）
        with open('turtle_soup_data.json', 'w', encoding='utf-8') as f:
            json.dump(soup_list, f, ensure_ascii=False, indent=4)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(scrape_soup())
