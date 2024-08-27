import allure
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from common.browser import BaseBrowser
from common.decorator import capture_screenshot_after_step
from common.platform import Platform


class SearchPage(BasePage):

    all_elements = {
        Platform.WEB: {
            "search_bar": (By.XPATH, '//input[@type="search"]'),
            "search_result_category": (By.XPATH, "//a[contains(@href, '/directory/category') and contains(@href, '{}')]")
        },
        Platform.ANDROID: {

        },
        Platform.IOS: {

        }
    }

    def __init__(self, browser: BaseBrowser):
        super().__init__(browser.get_driver())
        self.elements = self.all_elements[browser.platform]

    @capture_screenshot_after_step
    @allure.step("Input {text} in search bar")
    def input_value_in_search_bar(self, text: str):
        self.input_values(self.elements["search_bar"], text)

    @capture_screenshot_after_step
    @allure.step("Click search {text} result with type of category")
    def click_search_result_with_category(self, text: str):
        search_result_category = (
            self.elements["search_result_category"][0],
            self.elements["search_result_category"][1].format(text.replace(' ', '-').lower())
        )
        self.click_on_element(search_result_category)

