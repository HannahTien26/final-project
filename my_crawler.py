import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TurtleSoup 

def run_spider():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ptt.cc/bbs/TurtleSoup/index.html")
    
    posts = driver.find_elements(By.CLASS_NAME, "r-ent")
    links = [post.find_element(By.TAG_NAME, "a").get_attribute("href") for post in posts]
    
    engine = create_engine(os.environ.get("DATABASE_URL"))
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for link in links[:10]:
        driver.get(link)
        content = driver.find_element(By.ID, "main-content").text
        
        parts = content.split("解答")
        title = parts[0].split("\n")[0]
        answer = parts[1] if len(parts) > 1 else "無"
        
        new_entry = TurtleSoup(title=title, content=answer)
        session.add(new_entry)
        
    session.commit()
    session.close()
    driver.quit()

if __name__ == "__main__":
    run_spider()