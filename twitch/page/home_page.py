import allure
from selenium.webdriver.common.by import By
from selenium import webdriver

from common.base_page import BasePage
from common.decorator import capture_screenshot_after_step


class HomePageElement:

    elements = {
        "web": {
            "search_icon": (By.XPATH, '//a[@href="/search"]')
        },
        "android": {

        },
        "ios": {

        }
    }


class HomePage(BasePage):

    def __init__(self, driver: webdriver, platform: str):
        super().__init__(driver)
        self.__dict__.update(HomePageElement.elements.get(platform))

    @capture_screenshot_after_step
    @allure.step("Go to Twitch")
    def go_to_twitch(self):
        self.driver.get("https://m.twitch.tv/")

    @capture_screenshot_after_step
    @allure.step("Click in the search icon")
    def click_search_icon(self):
        """this will go to search page"""
        self.click_on_element(self.search_icon)
