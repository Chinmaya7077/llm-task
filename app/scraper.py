from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_visible_text(url: str) -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)

        full_text = driver.find_element("tag name", "body").text

        # 🔑 Reduce noise (critical for small models)
        lines = full_text.split("\n")
        cleaned = [
            line for line in lines
            if any(k in line.lower() for k in ["hard", "winter", "cash", "basis", "futures"])
        ]

        return "\n".join(cleaned)

    finally:
        driver.quit()

