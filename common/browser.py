import time
from enum import Enum
from appium import webdriver as appium_webdriver
from appium.options.common import AppiumOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from common.platform import Platform
from config import APP_IMPLICITLY_WAIT_TIME


class MobileDevices(Enum):
    PIXEL_7 = "Pixel 7"
    IPHONE_SE = "iPhone SE"
    IPHONE_14_PRO_MAX = "iPhone 14 Pro Max"
    IPAD_AIR = "iPad Air"


class SDK(Enum):
    APPIUM = 'Appium'
    # LAMBDATEST = 'LambdaTest'  # uncomment if support


class BaseBrowser:
    def __init__(self, options: ChromeOptions = None, platform: Platform = None):
        if not Platform:
            raise ValueError("Platform should be determined.")
        self.platform = platform
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.delete_all_cookies()

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()


class BaseApp:
    def __init__(self, capabilities: dict, sdk_env: SDK, platform: Platform = None):
        if not Platform:
            raise ValueError("Platform should be determined.")
        if Platform == Platform.WEB:
            raise ValueError("Platform should not be Web for APP test, Android iOS only.")
        self.platform = platform
        self.driver = AppiumWebdriverAndroid(capabilities, sdk_env).driver

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AppiumWebdriverAndroid(metaclass=Singleton):

    def __init__(self, capabilities: dict, sdk_env: SDK):
        self.data = capabilities
        self.driver = None
        if sdk_env == SDK.APPIUM:
            print("desired_capabilities: ", capabilities)
            appium_options = AppiumOptions()
            appium_options.load_capabilities(capabilities)
            # time.sleep(3)  # 等待 appium server 起好
            url = 'http://localhost:4723'
            self.driver = appium_webdriver.Remote(command_executor=url, options=appium_options)
            self.driver.implicitly_wait(APP_IMPLICITLY_WAIT_TIME)
        else:
            raise EnvironmentError(f"ANDROID_ENV 環境變數沒有設定正確，當前為: {sdk_env}")


if __name__ == "__main__":
    assert (MobileDevices.PIXEL_7.value == "Pixel 7")
