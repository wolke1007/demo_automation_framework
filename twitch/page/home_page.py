import allure
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from common.base_page import BasePage
from common.browser import BaseBrowser
from common.decorator import capture_screenshot_after_step
from common.platform import Platform


class HomePage(BasePage):
    all_elements = {
        Platform.WEB: {
            "search_icon": {
                BasePage.LOCATOR: (By.XPATH, '//a[@href="/search"]'),
            }
        },
        Platform.ANDROID: {

        },
        Platform.IOS: {

        }
    }

    def __init__(self, browser: BaseBrowser):
        project_name = self.get_project_name(__file__)
        super().__init__(browser.get_driver(), project_name)
        self.element_locators = self.all_elements[browser.platform]  # 依照 platform 決定元素

    @capture_screenshot_after_step
    @allure.step("Go to Twitch")
    def go_to_twitch(self):
        self.driver.get("https://m.twitch.tv/")

    @capture_screenshot_after_step
    @allure.step("Click in the search icon")
    def click_search_icon(self):
        """this will go to search page"""
        self.click_on_element(self.elements["search_icon"][self.LOCATOR])
