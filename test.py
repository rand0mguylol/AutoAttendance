from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, NoAlertPresentException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging, os

element = 'ion-button'
link = "https://apspace.apu.edu.my/login"

#Disable website launching
#options.add_argument("headless")

#Launching the browser
browser_option = "firefox"
browser = None
if browser_option == "chrome":
  #Webdriver options
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  browser = webdriver.Chrome(options=options, executable_path="./chromedriver.exe")

elif browser_option == "edge":
  browser = webdriver.Edge(executable_path="./msedgedriver.exe",)

elif browser_option == "firefox":
  profile = webdriver.FirefoxProfile()
  profile.set_preference("useAutomationExtension", False)
  profile.update_preferences()
  desired = DesiredCapabilities.FIREFOX
  browser = webdriver.Firefox(executable_path="./geckodriver.exe", firefox_profile=profile, service_log_path=os.devnull, desired_capabilities=desired)

else:
  logging.error(f"browser {browser_option} is not in the list")
  exit()

browser.get(link)

browser.implicitly_wait(10)

WebDriverWait(browser, 15).until(EC.url_to_be(link))
print("Clicking button")
get_ion_button = browser.find_elements_by_tag_name(element)
actions = ActionChains(browser)
actions.move_to_element(get_ion_button[1]).perform()
get_ion_button[1].click()

# WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, get_ion_button[1])))
# get_ion_button[1].click()

get_apkey = browser.find_elements_by_name("apkey")
get_password = browser.find_elements_by_name("password")

# logging.info("Logging in")
# get_apkey[1].send_keys(credential["tp"])
# get_password[1].send_keys(credential["pass"])
# get_ion_button[2].click()

# try:
#   link_2 = "https://apspace.apu.edu.my/tabs/dashboard"
#   WebDriverWait(browser, 15).until(EC.url_to_be(link_2))
#   get_all_button = browser.find_elements_by_tag_name(element)
#   get_all_button[3].click()

# except(StaleElementReferenceException):
#   link_2 = "https://apspace.apu.edu.my/tabs/dashboard"
#   WebDriverWait(browser, 15).until(EC.url_to_be(link_2))
#   get_all_button = browser.find_elements_by_tag_name(element)
#   get_all_button[3].click()


# link_3 = "https://apspace.apu.edu.my/attendix/update"
# WebDriverWait(browser,15).until(EC.url_to_be(link_3))
# get_input = browser.find_elements_by_tag_name("input")