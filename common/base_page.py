from enum import Enum
from pathlib import Path
from typing import Final

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from common.platform import Platform
from config import WEB_POLL_FREQUENCY
from common.wait_type import WaitType
import hashlib
import time
import logging


class BasePage:

    LOCATOR: Final = "locator"
    SCREENSHOT: Final = "screenshot"

    # sample
    all_elements = {
        Platform.WEB: {
            "demo": {
                LOCATOR: (By.XPATH, '//demo'),
                SCREENSHOT: 'target_pics/home_page/web_demo.jpg'  # 截圖以 web_ 開頭，代表 web 的截圖
            },
            "demo2": {
                LOCATOR: (By.XPATH, '//demo2'),
                # SCREENSHOT 為選填，該元素也可以沒有截圖，像是這個 demo2
                # 通常是需要使用截圖來當作判斷依據進行「點擊」或「驗證」才需要有
            }
        },
        Platform.ANDROID: {
            "demo": {
                LOCATOR: (By.XPATH, '//demo3'),
                SCREENSHOT: 'target_pics/home_page/android_demo.jpg'  # 截圖以 android_ 開頭，代表 android 的截圖
            },
        },
        Platform.IOS: {
            "demo": {
                LOCATOR: (By.XPATH, '//demo4'),
                SCREENSHOT: 'target_pics/home_page/ios_demo.jpg'  # 截圖以 ios_ 開頭，代表 ios 的截圖
            }
        },
    }

    def __init__(self, driver: webdriver, project_name):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.project_name = project_name.lower()
        self.__elements = {}

    def get_project_name(self, file):
        # 取得當前檔案的絕對路徑
        current_file_path = Path(file).resolve()
        # 取得專案根目錄
        project_root = current_file_path.parent.parent
        project_name = project_root.stem.lower()
        return project_name

    @property
    def elements(self):
        if self.__elements:  # 如果 _elements 不為空則直接返回，不重複執行
            return self.__elements

        # 动态生成包含 project_name 的元素字典并更新到 _elements
        for element_name, element_dict in self.element_locators.items():
            if element_dict.get("screenshot") is not None:
                # 更新元素的 screenshot 路径
                updated_screenshot_path = f"{self.project_name}/{element_dict['screenshot']}"
                element_dict["screenshot"] = updated_screenshot_path

            # 更新 _elements 字典
            self.__elements[element_name] = element_dict

        return self.__elements

    def wait_element_by(self, wait_type, element, timeout: float = 10):
        if wait_type is WaitType.VISIBILITY:
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.visibility_of_element_located(element)
            )
        elif wait_type is WaitType.CLICKABLE:
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.element_to_be_clickable(element)
            )
        elif wait_type is WaitType.INVISIBILITY:
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.invisibility_of_element_located(element)
            )
        elif wait_type is WaitType.PRESENCE:
            return WebDriverWait(self.driver, timeout, poll_frequency=WEB_POLL_FREQUENCY).until(
                EC.presence_of_element_located(element)
            )
        else:
            raise ValueError("wait_type not support!")

    def click_on_clickable_element(self, element):
        self.wait_element_by(WaitType.CLICKABLE, element)
        action = ActionChains(self.driver)
        action.click(on_element=self.driver.find_element(*element))
        action.perform()

    def click_on_element(self, element):
        self.wait_element_by(WaitType.VISIBILITY, element)
        action = ActionChains(self.driver)
        action.click(on_element=self.driver.find_element(*element))
        action.perform()

    def input_values(self, element, value):
        self.wait_element_by(WaitType.VISIBILITY, element)
        self.driver.find_element(*element).clear()
        self.driver.find_element(*element).send_keys(value)

    def scroll_by_offset(self, x_offset: int = 0, y_offset: int = 0):
        self.driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", x_offset, y_offset)

    def get_element_text(self, element):
        self.wait_element_by(WaitType.VISIBILITY, element)
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
