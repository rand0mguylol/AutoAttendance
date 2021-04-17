import win32gui
import win32ui #type: ignore
from ctypes import windll
from PIL import Image
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, NoAlertPresentException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time



def screenshot(application_name="Microsoft Teams"):
  toplist, winlist = [], []
  def enum_cb(hwnd, results):
      winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
  win32gui.EnumWindows(enum_cb, toplist)

  window = [(hwnd, title) for hwnd, title in winlist if application_name.lower() in title.lower() and "notification" not in title.lower()]
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
  # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
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

credential = json.load(open("./credential.json", "r"))


element = 'ion-button'
link = "https://apspace.apu.edu.my/login"

#Webdriver options
options = webdriver.ChromeOptions() 

#Disable website launching
#options.add_argument("headless")

#Disable getting the bluetooth adapter
options.add_experimental_option("excludeSwitches", ["enable-logging"])

#Launching the browser
browser = webdriver.Chrome(options=options, executable_path="./chromedriver.exe")
browser.get(link)


browser.implicitly_wait(5)

browser.maximize_window()

WebDriverWait(browser, 15).until(EC.url_to_be(link))
get_ion_button = browser.find_elements_by_tag_name(element)
# get_button = get_ion_button[1]

# get_button.click()
get_ion_button[1].click()

get_apkey = browser.find_elements_by_name("apkey")
get_password = browser.find_elements_by_name("password")


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


while True:
  time.sleep(2)
  img = screenshot()
  results = decode(img)
  if len(results) > 0:
    code = results[0].data.decode()
    code_list = list(code)
    for i in range(3):
      get_input[i+1].send_keys(code_list[i])
    try:
      WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.TAG_NAME, "ion-alert")))
      click_button = browser.find_element_by_class_name("alert-button").click()
      print("no")
    except:
      pass