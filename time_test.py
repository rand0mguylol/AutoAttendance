from pywinauto.application import Application
import pywinauto
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def join_team():
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  browser = webdriver.Chrome(options=options, executable_path="chromedriver.exe")

  link = r""
  browser.get(link)

  app = Application(backend="uia")
  # Find window with the word Microsoft Teams
  elem = ""
  while not(elem):
    elem = pywinauto.findwindows.find_element(title="Join conversation - Google Chrome")

  print(elem)
  app.connect(handle=elem.handle)
  print(app.windows())

  print("done")

  # Find the correct window
  win = app.window(title="Open Microsoft Teams?")

  # Wait for window to exist
  win.wait("exists enabled visible ready", timeout = 31, retry_interval=3)

  win["Open Microsoft Teams"].click()

  # Find window with the word Microsoft Teams
  elem = pywinauto.findwindows.find_elements(title_re=".*Microsoft Teams")
  app.connect(handle=elem[0].handle)

  # Find the correct window
  win = app.window(title_re=".* \| Microsoft Teams")

  # Wait for window to exist
  win.wait("exists enabled visible ready", timeout = 31, retry_interval=3)

  # Get the join button
  join_button = win.child_window(auto_id="prejoin-join-button")

  join_button.click()



sched = BackgroundScheduler()
sched.start()

sched.add_job(join_team, "date", run_date="2022-1-30 15:08:55", args=None)


while (True):
  jobs = sched.get_jobs()
  if not(jobs):
    break

sched.shutdown()
