# import pytesseract
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, NoAlertPresentException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

credential = json.load(open("./credential.json", "r"))

# get image
img = Image.open("D://NeuralNetwork//Screenshot (259).png")
results = decode(img)
code = results[0].data.decode()
code_list = list(code)


element = 'ion-button'
link = "https://apspace.apu.edu.my/login"

#Webdriver options
options = webdriver.ChromeOptions() 

#Disable website launching
#options.add_argument("headless")

#Disable getting the bluetooth adapter
options.add_experimental_option("excludeSwitches", ["enable-logging"])

#Launching the browser
browser = webdriver.Chrome(options=options, executable_path="C:\\Users\\user\\ChromeWebdriver\\chromedriver.exe")
browser.get(link)


browser.implicitly_wait(5)

# WebDriverWait(browser,15).until(EC.url_to_be(link))
browser.maximize_window()

WebDriverWait(browser, 15).until(EC.url_to_be(link))
get_ion_button = browser.find_elements_by_tag_name(element)
# get_button = get_ion_button[1]
# print(get_ion_button)

# get_button.click()
get_ion_button[1].click()

get_apkey = browser.find_elements_by_name("apkey")
get_password = browser.find_elements_by_name("password")
# get_ion_input = browser.find_elements_by_tag_name("ion-input")
print(get_apkey)
print(get_password)

get_apkey[1].send_keys(credential["tp"])
get_password[1].send_keys(credential["pass"])

# get_green_login = get_ion_button[2]
# get_green_login.click()
get_ion_button[2].click()


try:
  link_2 = "https://apspace.apu.edu.my/tabs/dashboard"
  WebDriverWait(browser, 15).until(EC.url_to_be(link_2))
  get_all_button = browser.find_elements_by_tag_name(element)
  get_all_button[3].click()

except(StaleElementReferenceException):
  link_2 = "https://apspace.apu.edu.my/tabs/dashboard"
  WebDriverWait(browser, 15).until(EC.url_to_be(link_2))
  get_all_button = browser.find_elements_by_tag_name(element)
  get_all_button[3].click()


link_3 = "https://apspace.apu.edu.my/attendix/update"
WebDriverWait(browser,15).until(EC.url_to_be(link_3))
get_input = browser.find_elements_by_tag_name("input")
print(get_input)


for i in range(3):
  get_input[i+1].send_keys(code_list[i])
