import os
import certifi
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()

# Locale Indonesia (bisa ditaruh di utils juga)
import locale
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except locale.Error:
    print("⚠ Locale 'id_ID.UTF-8' tidak tersedia, gunakan default.")

# Konfigurasi Gmail
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Konfigurasi Trello API
API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# Konfigurasi WhatsApp
NOMOR_WHATSAPP = os.getenv("WHATSAPP_NUMBER")

# Selenium
CHROME_DRIVER_PATH = "C:/Users/nanda/chromedriver/chromedriver.exe"
PROFILE_PATH = r"C:\Users\nanda\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Profile 2"
