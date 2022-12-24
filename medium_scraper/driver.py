from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class WebDriver:
    def __init__(self):
        self.options = Options()
        #self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        #self.options.add_argument('--single-process')
        # self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = webdriver.Chrome(options=self.options)
        return driver
