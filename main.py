import os
import win32gui
import win32ui #type: ignore
from ctypes import windll
from PIL import Image
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import json
import time

import logging

logging.basicConfig(level=logging.INFO)

INTERVAL_TIME = 1
credential = json.load(open("./credential.json", "r"))
option = json.load(open("./option.json", "r"))

def screenshot(application_name:str="Microsoft Teams"):
  toplist, winlist = [], []
  def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
  win32gui.EnumWindows(enum_cb, toplist)

  window = [(hwnd, title) for hwnd, title in winlist if application_name.lower() in title.lower() and "notification" not in title.lower()]
  if len(window) < 1:
    logging.debug(f"{application_name} not found in `winlist`!")
    return None

  # just grab the hwnd for first window matching window
  window = window[0]
  hwnd = window[0]

  # Change the line below depending on whether you want the whole window
  # or just the client area. 
  # left, top, right, bot = win32gui.GetClientRect(hwnd)
  left, top, right, bot = win32gui.GetWindowRect(hwnd)
  w = right - left
  h = bot - top

  hwndDC = win32gui.GetWindowDC(hwnd)
  mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
  saveDC = mfcDC.CreateCompatibleDC()

  saveBitMap = win32ui.CreateBitmap()
  saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

  saveDC.SelectObject(saveBitMap)

  # Change the line below depending on whether you want the whole window
  # or just the client area. 
  result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

  bmpinfo = saveBitMap.GetInfo()
  bmpstr = saveBitMap.GetBitmapBits(True)

  im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

  win32gui.DeleteObject(saveBitMap.GetHandle())
  saveDC.DeleteDC()
  mfcDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, hwndDC)

  if result == 1:
    #PrintWindow Succeeded
    # im.show()
    return im
  else:
    return None


element = 'ion-button'
attendance_element = "quick-access-attendance"
link = "https://apspace.apu.edu.my/login"

#Disable website launching
#options.add_argument("headless")

#Launching the browser
browser_option = option["browser"]
browser = None
if browser_option == "chrome":
  #Webdriver options
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  browser = webdriver.Chrome(ChromeDriverManager().install())

elif browser_option == "edge":
  browser = webdriver.Edge(EdgeChromiumDriverManager().install())

elif browser_option == "firefox":
  profile = webdriver.FirefoxProfile()
  profile.set_preference("useAutomationExtension", False)
  profile.update_preferences()
  desired = DesiredCapabilities.FIREFOX
  firefoxOption = Options
  browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile, service_log_path=os.devnull, desired_capabilities=desired)

else:
  logging.error(f"browser {browser_option} is not in the list")
  exit()

browser.get(link)

browser.implicitly_wait(10)

WebDriverWait(browser, 15).until(EC.url_to_be(link))
get_ion_button = browser.find_elements_by_tag_name(element)
if browser_option == "firefox":
  actions = ActionChains(browser)
  actions.move_to_element(get_ion_button[1]).perform()
get_ion_button[1].click()

get_apkey = browser.find_elements_by_name("apkey")
get_password = browser.find_elements_by_name("password")

logging.info("Logging in")
get_apkey[1].send_keys(credential["tp"])
get_password[1].send_keys(credential["pass"])
get_ion_button[2].click()

try:
  link_2 = "https://apspace.apu.edu.my/tabs/dashboard"
  WebDriverWait(browser, 15).until( EC.element_to_be_clickable((By.CLASS_NAME, attendance_element)))
  get_attendance_button = browser.find_element_by_class_name(attendance_element)
  get_attendance_button.click()

except(StaleElementReferenceException):
  link_2 = "https://apspace.apu.edu.my/tabs/dashboard"
  WebDriverWait(browser, 15).until( EC.element_to_be_clickable((By.CLASS_NAME, attendance_element)))
  get_attendance_button = browser.find_element_by_class_name(attendance_element)
  get_attendance_button.click()



link_3 = "https://apspace.apu.edu.my/attendix/update"
WebDriverWait(browser,15).until(EC.url_to_be(link_3))
get_input = browser.find_elements_by_tag_name("input")

while True:
  time.sleep(INTERVAL_TIME)
  img = screenshot()
  if not img:
    logging.debug("There is no screenshot!")
    continue
  results = decode(img)
  if len(results) < 1:
    logging.debug("QR Code not found!")
    continue

  code = results[0].data.decode()
  code_list = list(code)
  logging.info("QR code found!")
  for i in range(3):
    get_input[i+1].send_keys(code_list[i])
  try:
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.TAG_NAME, "ion-alert")))
    click_button = browser.find_element_by_class_name("alert-button").click()
    logging.debug("Clicked OK button")
  except Exception as e:
    logging.error(f"Error encountered: {e}")