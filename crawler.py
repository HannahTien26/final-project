import asyncio
from playwright.async_api import async_playwright
import psycopg2

async def crawl_ptt_turtle_soup():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page()
        await page.goto('https://www.ptt.cc/bbs/TurtleSoup/index.html')
        await page.wait_for_load_state('networkidle')
        divs = await page.query_selector_all('.r-ent')
        soup_links = []
        for div in divs:
            title_element = await div.query_selector('.title a')
            if title_element:
                title = await title_element.inner_text()
                href = await title_element.get_attribute('href')
                soup_links.append({"title": title, "url": f"https://www.ptt.cc{href}"})
            if len(soup_links) >= 10: break

        all_data = []
        for item in soup_links:
            await page.goto(item['url'])
            await page.wait_for_load_state('networkidle')
            main_content = await page.query_selector('#main-content')
            question = await main_content.inner_text() if main_content else ""
            all_data.append((item['title'], item['url'], question.strip()))
            await page.wait_for_timeout(500)
        await browser.close()
        
        db_url = "postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k"
        
        print("正在連接資料庫並寫入海龜湯資料...")
        try:
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS turtle_soups (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    url TEXT UNIQUE,
                    content TEXT
                );
            """)
            
            for title, url, content in all_data:
                cur.execute("""
                    INSERT INTO turtle_soups (title, url, content) 
                    VALUES (%s, %s, %s)
                    ON CONFLICT (url) DO NOTHING;
                """, (title, url, content))
                
            conn.commit()
            cur.close()
            conn.close()
            print("資料庫寫入成功！")
        except Exception as e:
            print(f"資料庫連線或寫入失敗，原因: {e}")

if __name__ == "__main__":
    asyncio.run(crawl_ptt_turtle_soup())