from pathlib import Path

import allure
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from common.base_page import BasePage
from common.browser import BaseBrowser
from common.decorator import capture_screenshot_after_step
from common.platform import Platform
from common.wait_type import WaitType


class HomePage(BasePage):

    all_elements = {
        Platform.WEB: {
            "demo": {
                BasePage.LOCATOR: (By.XPATH, 'aaa'),
                BasePage.SCREENSHOT: 'target_pics/home_page/web_demo.jpg'
            },
            "demo2": {
                BasePage.LOCATOR: (By.XPATH, 'aaa'),
            }
        },
        Platform.ANDROID: {
            "demo": {
                BasePage.LOCATOR: (By.ID, 'bbb'),
                BasePage.SCREENSHOT: 'target_pics/home_page/android_demo.jpg'
            }
        },
        Platform.IOS: {
            "demo": {
                BasePage.LOCATOR: (AppiumBy.IOS_CLASS_CHAIN, 'ccc'),
                BasePage.SCREENSHOT: 'target_pics/home_page/ios_demo.jpg'
            }
        }
    }

    def __init__(self, browser: BaseBrowser):
        project_name = self.get_project_name(__file__)
        super().__init__(browser.get_driver(), project_name)
        self.element_locators = self.all_elements[browser.platform]  # 依照給定的 platform 決定使用的元素

    @capture_screenshot_after_step
    @allure.step("Check into FatGoose game")
    def go_to_fat_goose(self):
        self.wait_element_by(WaitType.VISIBILITY, self.elements['content'])

    def test_demo(self):
        print(self.elements['demo'][self.LOCATOR])


if __name__ == "__main__":
    b = BaseBrowser(platform=Platform.WEB)
    hp = HomePage(b)
    hp.test_demo()
