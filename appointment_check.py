from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from plyer import notification
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

# Config
URL = "https://service.berlin.de/terminvereinbarung/termin/taken/"
CHECK_INTERVAL = 180  # seconds

def notify(title, message):
  token = os.getenv('TELEGRAM_BOT_TOKEN')
  chat_id = os.getenv('TELEGRAM_CHAT_ID')
  text = f"📢 {title}\n{message}\n\n🔗 {URL}"

  try:
      requests.post(
          f"https://api.telegram.org/bot{token}/sendMessage",
          data={"chat_id": chat_id, "text": text}
      )
  except Exception as e:
      print("❌ Telegram error:", e)

def check_appointments():
    options = Options()
    options.headless = True  # Don't open browser window
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)
        time.sleep(5)  # Let page load

        page_text = driver.page_source

        if (
            "Unfortunately, there are currently no dates available for your selection." in page_text or
            "Leider sind aktuell keine Termine für ihre Auswahl verfügbar." in page_text
        ):
            print("❌ No appointment available.")
        else:
            notify("📅 Berlin Appointment", "Slot might be available – check now!")
            print("✅ Slot might be available!")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

# Run periodically
while True:
    check_appointments()
    time.sleep(CHECK_INTERVAL)
