import os
import time
import pytest
import allure
from config import TWITCH_PIC_DIR
from twitch.page.home_page import HomePage
from twitch.page.search_page import SearchPage
from twitch.page.category_page import CategoryPage
from twitch.page.streamer_home_page import StreamerHomePage

# 参数化
parameter_list = [
    {
        "platform": "web",
        "search_subject": "StarCraft II",
        "scroll_up_times": 2,
        "streamer_index": 1,
    },
]


class TestTwitch:

    @pytest.mark.wap_regression
    @allure.testcase('Web Regression Test')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Twitch Web Automation Testing")
    @allure.feature("Streamer Search and Screenshot")
    @allure.story("Search StarCraft II Streamer and Take Screenshot")
    @pytest.mark.parametrize("parameter", parameter_list)
    def test_twitch_wap_001(self, get_base_browser_driver, parameter):
        driver = get_base_browser_driver
        platform = parameter['platform']

        with allure.step("Twitch Home Page"):
            home_page = HomePage(driver, platform)
            home_page.go_to_twitch()
            home_page.click_search_icon()

        with allure.step("Search Page"):
            search_page = SearchPage(driver, platform)
            search_page.input_value_in_search_bar(parameter['search_subject'])
            search_page.click_search_result_with_category(parameter['search_subject'])

        with allure.step("Category Page"):
            category_page = CategoryPage(driver, platform)
            category_page.scroll_up(parameter['scroll_up_times'])
            category_page.click_index_streamer(parameter['streamer_index'])

        with allure.step("Streamer Home Page"):
            stream_home_page = StreamerHomePage(driver, platform)
            stream_home_page.wait_for_streamer_page_loaded()

        with allure.step("Save Screenshot"):
            # save screenshot
            formatted_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            filename = os.path.join(TWITCH_PIC_DIR, f'{formatted_time}_first_streamer_home_page.png')
            driver.save_screenshot(filename)
