import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# --- TARGET CONFIGURATION ---
BLOG_POST_URL = "https://burraq-vision.blogspot.com/2025/12/cheap-car-insurance-usa-2025.html"

# --- FAKE PERSONAS (Locations & Devices) ---
LOCATIONS = [
    {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060, "tz": "America/New_York", "lang": "en-US"},
    {"name": "London, UK", "lat": 51.5074, "lon": -0.1278, "tz": "Europe/London", "lang": "en-GB"},
    {"name": "Los Angeles, USA", "lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles", "lang": "en-US"},
    {"name": "Chicago, USA", "lat": 41.8781, "lon": -87.6298, "tz": "America/Chicago", "lang": "en-US"},
    {"name": "Dallas, USA", "lat": 32.7767, "lon": -96.7970, "tz": "America/Chicago", "lang": "en-US"}
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
]

def setup_driver(location_data):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled') # Bot detection bypass
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    
    driver = webdriver.Chrome(options=options)
    
    # --- JHOOTI LOCATION SET KARNA ---
    params = {
        "latitude": location_data["lat"], 
        "longitude": location_data["lon"], 
        "accuracy": 100
    }
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": location_data["tz"]})
    
    return driver

def human_scroll(driver):
    """Insani Scroll: Thora neechay, thora rukna, wapis upar dekhna"""
    print("   📜 Reading article like a human...")
    total_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll = 0
    
    while current_scroll < total_height:
        scroll_step = random.randint(300, 600)
        current_scroll += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(random.uniform(1, 3)) # Parhne ka waqt
        
        # Kabhi kabhi wapis upar scroll karna (Real behavior)
        if random.random() < 0.2:
            driver.execute_script(f"window.scrollBy(0, -200);")
            time.sleep(1)
        
        try:
            driver.find_element(By.ID, "magic-btn")
            print("   🎯 Button Found!")
            break
        except:
            pass

def run_single_cycle():
    # Har baar nayi location aur naya bhes
    chosen_loc = random.choice(LOCATIONS)
    print(f"\n🚀 New Visitor Starting from: {chosen_loc['name']}")
    
    driver = setup_driver(chosen_loc)
    
    try:
        # Step 1: Blog Visit
        driver.get(BLOG_POST_URL)
        time.sleep(random.randint(5, 8))
        
        # Step 2: Parhna (Scroll)
        human_scroll(driver)
        
        # Step 3: Button Click
        try:
            button = driver.find_element(By.ID, "magic-btn")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(2)
            
            print("   💰 CLICKING AD...")
            driver.execute_script("arguments[0].click();")
            
            # Note: Adsterra aksar naye tab mein khulta hai
            time.sleep(5)
            tabs = driver.window_handles
            if len(tabs) > 1:
                driver.switch_to.window(tabs[1]) # Naye tab (Ad) par jao
                print("   👀 Viewing Ad Page...")
                time.sleep(random.randint(30, 50)) # 30-50 second ruko taake paisay count hon
                driver.close() # Ad band karo
                driver.switch_to.window(tabs[0]) # Wapis blog par aao
            else:
                print("   👀 Viewing Ad on same page...")
                time.sleep(random.randint(30, 50))

            print("   ✅ Money Generated. Cycle Complete.")
            
        except Exception as e:
            print(f"   ⚠️ Button Click Issue: {e}")

    except Exception as e:
        print(f"   ❌ Error in cycle: {e}")
    finally:
        driver.quit() # Browser band karo taake history clear ho jaye

# --- INFINITE LOOP ENGINE ---
if __name__ == "__main__":
    print("🔥 BURRAQ ADSTERRA ENGINE STARTED 🔥")
    print("-----------------------------------")
    
    cycle_count = 1
    while True:
        print(f"🔄 Starting Batch #{cycle_count}")
        run_single_cycle()
        
        # Agle visitor ke aane se pehle thora break (Safety)
        rest_time = random.randint(10, 20)
        print(f"💤 Resting for {rest_time} seconds before next visitor...")
        time.sleep(rest_time)
        cycle_count += 1
