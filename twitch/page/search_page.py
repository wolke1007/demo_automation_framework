import allure
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from common.decorator import capture_screenshot_after_step


class SearchPageElement:
    elements = {
        "web": {
            "search_bar": (By.XPATH, '//input[@type="search"]'),
            "search_result_category": (By.XPATH, "//a[contains(@href, '/directory/category') and contains(@href, '{}')]")
        },
        "android": {

        },
        "ios": {

        }
    }


class SearchPage(BasePage):

    def __init__(self, driver, platform):
        super().__init__(driver)
        self.__dict__.update(SearchPageElement.elements.get(platform))

    @capture_screenshot_after_step
    @allure.step("Input {text} in search bar")
    def input_value_in_search_bar(self, text: str):
        self.input_values(self.search_bar, text)

    @capture_screenshot_after_step
    @allure.step("Click search {text} result with type of category")
    def click_search_result_with_category(self, text: str):
        search_result_category = (
            self.search_result_category[0],
            self.search_result_category[1].format(text.replace(' ', '-').lower())
        )
        self.click_on_element(search_result_category)


if __name__ == "__main__":
    element = SearchPageElement.elements['web']

