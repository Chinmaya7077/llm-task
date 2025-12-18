from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_visible_text(url: str) -> str:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)

        full_text = driver.find_element("tag name", "body").text
        print("\n================ FULL SCRAPED TEXT START ================\n")
        print(full_text)
        print("\n================ FULL SCRAPED TEXT END ==================\n")

        # 🔑 Reduce noise (critical for small models)
        lines = full_text.split("\n")
        KEYWORDS = [
        # Commodity (STRICT)
        "hard red winter",
        "hard red",
        "winter wheat",

        # Pricing table columns
        "cash",
        "basis",
        "futures",
        "future",
        "chg",

        # Delivery months (REQUIRED)
        "jan", "feb", "mar", "apr", "may", "jun",
        "jul", "aug", "sep", "oct", "nov", "dec",
        

        # Status
        "valid"
    ]

        cleaned = [
            line for line in lines
            if any(k in line.lower() for k in KEYWORDS)
        ]

        # return "\n".join(cleaned)

        cleaned_text = "\n".join(cleaned)

        print("=== CLEANED SCRAPED TEXT START ===")
        print(cleaned_text[:3000])
        print("=== CLEANED SCRAPED TEXT END ===")

        return cleaned_text

    finally:
        driver.quit()

