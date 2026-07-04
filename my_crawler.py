import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TurtleSoup

db_url = os.environ.get("postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2k")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

def run_spider():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ptt.cc/bbs/TurtleSoup/index.html")
    
    posts = driver.find_elements(By.CLASS_NAME, "r-ent")
    
    for post in posts:
        try:
            title = post.find_element(By.CLASS_NAME, "title").text
            
            new_data = TurtleSoup(title=title)
            session.add(new_data)
            session.commit()
            
        except:
            continue
            
    driver.quit()
    session.close()

if __name__ == "__main__":
    run_spider()