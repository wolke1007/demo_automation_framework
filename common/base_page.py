from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from config import WEB_POLL_FREQUENCY
import hashlib
import time
import logging


class BasePage:

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def wait_element_by(self, wait_type, element, timeout: float = 10):
        if wait_type == "visibility":
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.visibility_of_element_located(element)
            )
        elif wait_type == "clickable":
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.element_to_be_clickable(element)
            )
        elif wait_type == "invisibility":
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.invisibility_of_element_located(element)
            )
        elif wait_type == "presence":
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.presence_of_element_located(element)
            )
        else:
            raise ValueError("wait_type not support!")

    def click_on_clickable_element(self, element):
        self.wait_element_by("clickable", element)
        action = ActionChains(self.driver)
        action.click(on_element=self.driver.find_element(*element))
        action.perform()

    def click_on_element(self, element):
        self.wait_element_by("visibility", element)
        action = ActionChains(self.driver)
        action.click(on_element=self.driver.find_element(*element))
        action.perform()

    def input_values(self, element, value):
        self.wait_element_by("visibility", element)
        self.driver.find_element(*element).clear()
        self.driver.find_element(*element).send_keys(value)

    def scroll_by_offset(self, x_offset: int = 0, y_offset: int = 0):
        self.driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", x_offset, y_offset)

    def get_element_text(self, element):
        self.wait_element_by("visibility", element)
        return self.driver.find_element(*element).text

    def find_elements(self, element):

        def _is_element_obstructed(el):
            script = """
            var rect = arguments[0].getBoundingClientRect();
            var isInViewport = (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );

            if (!isInViewport) return false;

            // 检查是否被其他元素遮蔽
            var isCovered = Array.prototype.some.call(
                document.elementsFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2),
                function(el) {
                    return el !== arguments[0] && getComputedStyle(el).zIndex > getComputedStyle(arguments[0]).zIndex;
                }
            );

            return isCovered;
            """
            return self.driver.execute_script(script, el)

        elements = self.driver.find_elements(*element)

        # debug
        # selectors = [f'({element[1]})[{index}]' for index, _ in enumerate(elements, start=1)]
        # for element, selector in zip(elements, selectors):
        #     print(element.text, _is_element_obstructed(element))

        return [element for element in elements if not _is_element_obstructed(element)]

    def click_on_element_using_js(self, webelement: WebElement):
        self.driver.execute_script("arguments[0].click();", webelement)

    def is_page_all_pic_loaded(self, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return Array.from(document.images).every(img => img.complete);")
        )

    def _get_dom_hash(self):
        dom = self.driver.execute_script('return document.documentElement.outerHTML')
        return hashlib.md5(dom.encode('utf-8')).hexdigest()

    def wait_for_dom_stability(self, timeout=10, stability_time=2):
        initial_hash = self._get_dom_hash()
        end_time = time.time() + timeout

        while time.time() < end_time:
            time.sleep(stability_time)
            current_hash = self._get_dom_hash()
            if initial_hash == current_hash:
                return
            initial_hash = current_hash

        raise TimeoutException("DOM did not stabilize within the timeout period.")
