import logging

import pytest

from common.browser import BaseApp, SDK
from common.platform import Platform
from config import WEB_IMPLICITLY_WAIT_TIME


@pytest.fixture()
def get_base_app():
    # Appium 需要使用的
    capabilities = {
        "platformName": Platform.ANDROID.value,
        "automationName": "uiautomator2",
        "udid": "9A141FFAZ000VV",
        "platformVersion": "13",
        "deviceName": "Pixel 4",
        "appActivity": "org.cocos2dx.javascript.SplashActivity",
        "appPackage": "com.hortor.fejsf.asia",
        "noReset": True
    }
    base_app = BaseApp(capabilities, SDK.APPIUM, Platform.ANDROID)
    base_app.get_driver().implicitly_wait(WEB_IMPLICITLY_WAIT_TIME)
    yield base_app
    # The fixture first instantiates the browser driver, then returns it to the test case
    # (as a parameter). After performing the operations, it returns to the driver, and then proceeds to the next
    # step, closing the browser.
    base_app.get_driver().quit()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # can add a setup here
    logging.info(f"Setting up {item.name}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item):
    # can add a teardown here
    logging.info(f"Tearing down {item.name}")
