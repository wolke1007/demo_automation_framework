import allure
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from common.browser import BaseBrowser
from common.decorator import capture_screenshot_after_step
from common.platform import Platform
from common.wait_type import WaitType


class HomePage(BasePage):

    all_elements = {
        Platform.ANDROID: {
            "content": (By.ID, 'android:id/content')
        },
        Platform.IOS: {

        }
    }

    def __init__(self, browser: BaseBrowser):
        super().__init__(browser.get_driver())
        self.elements = self.all_elements[browser.platform]

    @capture_screenshot_after_step
    @allure.step("Check into FatGoose game")
    def go_to_fat_goose(self):
        self.wait_element_by(WaitType.VISIBILITY, self.elements['content'])