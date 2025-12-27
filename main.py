import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
BLOG_POST_URL = "https://burraq-vision.blogspot.com/2025/12/cheap-car-insurance-usa-2025.html"

# --- LOCATIONS ---
LOCATIONS = [
    {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060, "tz": "America/New_York"},
    {"name": "London, UK", "lat": 51.5074, "lon": -0.1278, "tz": "Europe/London"},
    {"name": "Los Angeles, USA", "lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles"},
    {"name": "Chicago, USA", "lat": 41.8781, "lon": -87.6298, "tz": "America/Chicago"},
    {"name": "Dallas, USA", "lat": 32.7767, "lon": -96.7970, "tz": "America/Chicago"}
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def setup_driver(location_data):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    
    driver = webdriver.Chrome(options=options)
    
    # Location Spoofing
    params = {"latitude": location_data["lat"], "longitude": location_data["lon"], "accuracy": 100}
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": location_data["tz"]})
    
    return driver

def safe_click(driver, element):
    """3-Layer Click System: Ye click miss nahi karega"""
    try:
        # Tareeka 1: Standard Click
        element.click()
        return True
    except:
        try:
            # Tareeka 2: JavaScript Click (Powerful)
            driver.execute_script("arguments[0].click();", element)
            return True
        except:
            try:
                # Tareeka 3: Action Chain Click (Mouse Move)
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
                return True
            except Exception as e:
                print(f"   ❌ All click methods failed: {e}")
                return False

def human_scroll(driver):
    print("   📜 Reading article like a human...")
    total_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll = 0
    
    while current_scroll < total_height:
        scroll_step = random.randint(400, 700)
        current_scroll += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Check agar button screen par aa gaya ho
        try:
            driver.find_element(By.ID, "magic-btn")
            break # Button mil gaya, scroll roko
        except:
            pass

def run_single_cycle():
    chosen_loc = random.choice(LOCATIONS)
    print(f"\n🚀 New Visitor Starting from: {chosen_loc['name']}")
    
    driver = setup_driver(chosen_loc)
    wait = WebDriverWait(driver, 15) # 15 second tak intezar karega
    
    try:
        driver.get(BLOG_POST_URL)
        time.sleep(5)
        
        human_scroll(driver)
        
        # --- BUTTON FINDING (Waiting Mode) ---
        try:
            print("   🔍 Looking for Magic Button...")
            # Ye line tab tak rukegi jab tak button load na ho jaye
            button = wait.until(EC.presence_of_element_located((By.ID, "magic-btn")))
            
            # Button ko screen ke beech mein lao
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(2)
            
            print("   🎯 Button Found! Attempting Click...")
            if safe_click(driver, button):
                print("   💰 CLICK SUCCESS! Ad Opened.")
                print("   ⏳ Watching Ad for 40 seconds...")
                time.sleep(random.randint(35, 45))
                print("   ✅ Money Generated.")
            else:
                print("   ⚠️ Click failed technically.")
                
        except Exception as e:
            print(f"   ⚠️ Button not found (Network Issue?): {e}")

    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🔥 BURRAQ SUPER BOT STARTED 🔥")
    while True:
        run_single_cycle()
        rest_time = random.randint(5, 15)
        print(f"💤 Sleeping {rest_time}s...")
        time.sleep(rest_time)
