import allure
from selenium.webdriver.common.by import By
from selenium import webdriver

from common.base_page import BasePage
from common.browser import BaseBrowser
from common.decorator import capture_screenshot_after_step
from common.platform import Platform
from common.wait_type import WaitType


class StreamerHomePage(BasePage):

    all_elements = {
        Platform.WEB: {
            "streamer_avatar": {
                BasePage.LOCATOR: (By.CSS_SELECTOR, 'div.Layout-sc-1xcs6mc-0.ilxZVe > div.Layout-sc-1xcs6mc-0.eWHdFL'),
            }
        },
        Platform.ANDROID: {},
        Platform.IOS: {}
    }

    def __init__(self, browser: BaseBrowser):
        project_name = self.get_project_name(__file__)
        super().__init__(browser.get_driver(), project_name)
        self.element_locators = self.all_elements[browser.platform]  # 依照 platform 決定元素

    @capture_screenshot_after_step
    @allure.step("Wait for streamer page loaded")
    def wait_for_streamer_page_loaded(self):
        self.wait_element_by(WaitType.VISIBILITY, self.elements["streamer_avatar"][self.LOCATOR])
        self.is_page_all_pic_loaded()
        self.wait_for_dom_stability()
