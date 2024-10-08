import allure
from selenium.webdriver.common.by import By
from common.base_page import BasePage
import time

from common.browser import BaseBrowser
from common.decorator import capture_screenshot_after_step
from common.platform import Platform


class CategoryPage(BasePage):

    all_elements = {
        Platform.WEB: {
            "category_title": (By.XPATH, '//div[@class="Layout-sc-1xcs6mc-0 eTMECT"]'),
            "streamer_names": (By.XPATH, '//a[@class="ScCoreLink-sc-16kq0mq-0 gpIqoK InjectLayout-sc-1i43xsx-0 fdCwys tw-link" and contains(@href, "/home")]'),
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
    @allure.step("Scroll up page for {times} times")
    def scroll_up(self, times: int = 1):
        self.wait_element_by("visibility", self.elements["category_title"])
        # 取得視窗的尺寸
        window_rect = self.driver.get_window_rect()
        window_height = window_rect['height']
        offset = window_height / 2
        for _ in range(times):
            self.scroll_by_offset(y_offset=offset)
            time.sleep(1)

    @capture_screenshot_after_step
    @allure.step("Click the {index}-th video from the top")
    def click_index_streamer(self, index: int = 1):
        self.wait_for_dom_stability()
        streamer_names = self.find_elements(self.elements["streamer_names"])
        if len(streamer_names) == 0 or index - 1 >= len(streamer_names):
            raise RuntimeError(f"length of streamer_names: {len(streamer_names)}")
        self.click_on_element_using_js(streamer_names[index - 1])
