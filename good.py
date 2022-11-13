from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from discord_webhook import DiscordWebhook, DiscordEmbed

n = "No hay ningún modelo de iPhone 14 Pro "
NOT_AVAILABLE = "No disponible hoy en "
POST_CODES = {"BARCELONA": "08007", "MADRID": "28025"}
WEBHOOK = "https://discord.com/api/webhooks/902460822641594378/dsKl0Ec-bW3J2Nori51XuLjbpRpcsRBO3qIWK03o9BQ4bXIzGQCejiFeGdNodCBmUCC0"


def send_message(message):
  try:
    webhook = DiscordWebhook(url=WEBHOOK)

    with open("./screenshot.png", "rb") as f:
      webhook.add_file(file=f.read(), filename='ss.png')

    embed = DiscordEmbed(title='IPHONE 14 PRO STOCK CHECKER',
                         description=message,
                         color=242424)

    embed.set_image(url='attachment://ss.png')

    webhook.add_embed(embed)
    webhook.execute()

  except Exception as e:
    print(e)


def create_driver(url):
  chromeOptions = Options()
  chromeOptions.add_argument('--no-sandbox')
  chromeOptions.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chromeOptions)

  driver.get(url)

  print("Driver created")

  return driver


def initial_actions(driver, wait):

  element = driver.find_element(By.ID, 'noTradeIn')
  element.click()
  print("Clicked no trade in button")

  wait.until(
      EC.visibility_of_element_located(
          (By.CSS_SELECTOR, "div.rf-po-bfe-dimension-base:nth-child(1)"))).click()
  print("Clicked buy button")

  wait.until(
      EC.visibility_of_element_located((
          By.XPATH,
          "/html/body/div[2]/div[4]/div[4]/div[3]/div[3]/div[3]/div/div/div[1]/div[1]/fieldset/div/div/div[5]"
      ))).click()
  print("Clicked no apple + button")
  wait.until(
      EC.visibility_of_element_located(
          (By.CSS_SELECTOR, ".rf-pickup-quote-overlay-trigger"))).click()
  print("Clicked pickup button")


def check_stock(driver, wait):

  for post_code in POST_CODES:
    print("Checking stock for " + post_code)

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             ".form-textbox > input"))).send_keys(Keys.BACKSPACE * 6,
                                                  POST_CODES[post_code],
                                                  Keys.ENTER)

    try:
      availabilty = wait.until(
          EC.visibility_of_element_located(
              (By.CSS_SELECTOR, ".rf-productlocator-suggestionitems"))).text

      if availabilty.startswith(n):

        print(f"NOT AVAILABLE IN {post_code}", "POST CODE: ",
              POST_CODES[post_code], "time and date:",
              time.asctime(time.localtime(time.time())))
    except NoSuchElementException:
      print(f"AVAILABLE IN {post_code}", "POST CODE: ", POST_CODES[post_code],
            "time and date:", time.asctime(time.localtime(time.time())))
      time.sleep(5)
      driver.save_screenshot('./screenshot.png')
      send_message("IPHONE 14 PRO IS AVAILABLE IN " + post_code +
                   ", POST CODE: " + POST_CODES[post_code] + "time and date:" +
                   time.asctime(time.localtime(time.time())))
      time.sleep(5)


def run():
  url = "https://www.apple.com/es/shop/buy-iphone/iphone-14-pro/pantalla-de-6,1%E2%80%B3-128gb-morado-oscuro"
  url = "https://www.apple.com/es/shop/buy-iphone/iphone-14/pantalla-de-6,1%E2%80%B3-128gb-p%C3%BArpura"
  driver = create_driver(url)
  wait = WebDriverWait(driver, 20)
  initial_actions(driver, wait)
  try:
    check_stock(driver, wait)
  except Exception as e:
    print(e)
    driver.quit()


if __name__ == "__main__":
  run()
