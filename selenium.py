import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_DRIVER_PATH, PROFILE_PATH, PROFILE_NAME

def init_driver():
    options = Options()
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    options.add_argument(f'--profile-directory={PROFILE_NAME}')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def buka_chat_me(driver):
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.clear()
        search_box.send_keys("Me (You)")
        search_box.send_keys(Keys.ENTER)
        print("✅ Berhasil membuka chat Me (You)")
    except Exception as e:
        print(f"❌ Gagal membuka chat Me (You): {e}")

def kirim_pesan(driver, nomor, pesan):
    try:
        pesan_encoded = pesan.replace("\n", "%0A")
        url = f"https://web.whatsapp.com/send?phone={nomor}&text={pesan_encoded}"
        driver.get(url)

        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab]"))
        )
        time.sleep(2)
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)
        print(f"✅ Pesan berhasil dikirim ke {nomor}")
    except Exception as e:
        print(f"❌ Gagal mengirim pesan ke {nomor}: {e}")
