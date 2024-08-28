import pytest
import allure

from common.platform import Platform
from fatgoose.page.home_page import HomePage

# 参数化
parameter_list = [
    {
        "platform": Platform.ANDROID,
    },
]


class TestFatGoose:

    @allure.testcase('Android Regression Test')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("parameter", parameter_list)
    def test_fat_goose_001(self, get_base_app, parameter):
        app = get_base_app

        with allure.step("Home Page"):
            home_page = HomePage(app)
            home_page.go_to_fat_goose()
