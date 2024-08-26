import logging
import pytest
from common.browser import BaseBrowser, MobileDevices
from selenium.webdriver import ChromeOptions
from config import WEB_IMPLICITLY_WAIT_TIME


@pytest.fixture()
def get_base_browser_driver():
    options = ChromeOptions()
    options.add_argument("window-size=1920x1080")
    # Remove the "Chrome is being controlled by automated test software" message
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('mobileEmulation', {'deviceName': MobileDevices.PIXEL_7.value})

    # Resolve issues with Selenium unable to access https
    options.add_argument("--ignore-certificate-errors")
    # Allow ignoring TLS/SSL errors on localhost
    options.add_argument("--allow-insecure-localhost")
    # Set to incognito mode
    options.add_argument("--incognito")
    # Set to headless mode
    # options.add_argument("--headless")
    # Solve stuttering with these three parameters
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Disable sandbox
    options.add_argument("--disable-dev-shm-usage")

    base_browser_driver = BaseBrowser(options).get_driver()
    base_browser_driver.implicitly_wait(WEB_IMPLICITLY_WAIT_TIME)

    yield base_browser_driver
    # The fixture first instantiates the browser driver, then returns it to the test case
    # (as a parameter). After performing the operations, it returns to the driver, and then proceeds to the next
    # step, closing the browser.
    base_browser_driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # can add a setup here
    logging.info(f"Setting up {item.name}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item):
    # can add a teardown here
    logging.info(f"Tearing down {item.name}")
