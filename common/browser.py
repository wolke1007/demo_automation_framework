from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions


class MobileDevices(Enum):

    PIXEL_7 = "Pixel 7"
    IPHONE_SE = "iPhone SE"
    IPHONE_14_PRO_MAX = "iPhone 14 Pro Max"
    IPAD_AIR = "iPad Air"


class BaseBrowser:
    def __init__(self, options: ChromeOptions = None):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.delete_all_cookies()

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    assert(MobileDevices.PIXEL_7.value == "Pixel 7")
