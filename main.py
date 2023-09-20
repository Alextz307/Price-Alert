from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import smtplib
import os

CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')

PRODUCT_URL = 'https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6'
REQUIRED_PRICE = 100  # $

service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.get(url=PRODUCT_URL)

price_whole = driver.find_element(By.CSS_SELECTOR, '.a-price-whole')
price_fraction = driver.find_element(By.CSS_SELECTOR, '.a-price-fraction')
complete_price = f'{price_whole.text}.{price_fraction.text}'

product_title = driver.find_element(By.CSS_SELECTOR, '#productTitle').text

if float(complete_price) < REQUIRED_PRICE:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)

        message_subject = 'Amazon price alert!'
        message_body = f'{product_title} is now only ${complete_price}: {PRODUCT_URL}'

        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs='alexandru.lorintz@yahoo.com',
            msg=f'Subject:{message_subject}\n\n{message_body}'.encode('utf-8')

        )

driver.quit()
