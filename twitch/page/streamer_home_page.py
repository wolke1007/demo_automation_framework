import allure
from selenium.webdriver.common.by import By
from selenium import webdriver

from common.base_page import BasePage
from common.decorator import capture_screenshot_after_step


class StreamerHomePageElement:

    elements = {
        "web": {
            "streamer_avatar": (By.CSS_SELECTOR, 'div.Layout-sc-1xcs6mc-0.ilxZVe > div.Layout-sc-1xcs6mc-0.eWHdFL')
        },
        "android": {

        },
        "ios": {

        }
    }


class StreamerHomePage(BasePage):

    def __init__(self, driver: webdriver, platform: str):
        super().__init__(driver)
        self.__dict__.update(StreamerHomePageElement.elements.get(platform))

    @capture_screenshot_after_step
    @allure.step("Wait for streamer page loaded")
    def wait_for_streamer_page_loaded(self):
        self.wait_element_by("visibility", self.streamer_avatar)
        self.is_page_all_pic_loaded()
        self.wait_for_dom_stability()