from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import uuid
from config import MONGO_URI,PATH

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['twitter_trends']
collection = db['trends']

# ProxyMesh credentials
from config import PROXY_USER, PROXY_PASS, TWITTER_USER, TWITTER_PASS
PROXY_URL = f'http://{PROXY_USER}:{PROXY_PASS}@us.proxymesh.com:31280'

# Chrome options with proxy setup
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'--proxy-server={PROXY_URL}')

# Selenium setup
service = Service(PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def fetch_twitter_trends():
    try:
        driver.get("https://twitter.com/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "session[username_or_email]"))
        )

        # Login
        username = driver.find_element(By.NAME, "session[username_or_email]")
        password = driver.find_element(By.NAME, "session[password]")
        username.send_keys(TWITTER_USER)
        password.send_keys(TWITTER_PASS)
        password.send_keys(Keys.RETURN)

        # Wait for the "What’s Happening" section
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section[contains(@aria-labelledby, 'accessible-list')]"))
        )

        # Fetch trending topics
        trends = driver.find_elements(By.XPATH, "//span[contains(text(),'#') or contains(text(),'trending')]")[:5]
        trending_topics = [trend.text for trend in trends]

        # Generate unique ID and fetch IP
        unique_id = str(uuid.uuid4())
        ip_address = driver.execute_script("return window.navigator.platform;")  # Mocking actual IP fetch for ProxyMesh

        # Store data in MongoDB
        result = {
            "unique_id": unique_id,
            "trends": trending_topics,
            "date_time": datetime.now(),
            "ip_address": ip_address
        }
        collection.insert_one(result)

        return result

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print(fetch_twitter_trends())
