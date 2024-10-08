# Automation Test Framework Demo

## Introduction
![Demo](doc/demo.gif)  
This is a demo project for WAP Test automation.  
The project utilizes frameworks such as Selenium, WebDriver Manager, Pytest, and Allure.  
It is designed with extensibility in mind for Android, iOS, WAP, and WEB testing.  
The results are recorded in an Allure report, and screenshots are taken at the end of each test step to facilitate debugging (screenshots can be disabled to improve execution speed).

## Running Tests
To execute test cases:
```
cd twitch

# Run WAP tests
pytest -m wap_regression

# Run Web tests
pytest -m web_regression
```

To view the Allure report:
```
# Ensure Allure is installed in your environment
# For macOS
brew install allure

# Run allure server, to see allure report in html 
allure serve ./allure_report
```

## Project Extension
1. The project is written using the PageObject pattern. You can add new pages in `{product_name}/page`, for example, `twitch/page`.
2. In each Page, `elements` represents the DOM elements available for interaction or location. They are recorded in a dictionary and categorized into web/android/ios to allow reuse across platforms without rewriting PageObjects.
3. Operations occurring on a Page are written in that Page, with `allure.step` used before each function to document the test steps.
4. Add new TestCases in `{product_name}/testcase/{platform}`, for example, `twitch/testcase/wap`.

## Project Structure
```
.
├── README.md
├── common
│   ├── __init__.py    <-- Shared components
│   ├── base_page.py
│   ├── browser.py
│   ├── decorator.py
│   └── platform.py
├── config    <-- Global variable settings
│   └── __init__.py
├── doc    <-- Files used for README.md
│   └── demo.gif
├── requirements.txt
└── twitch    <-- Project directory; if you want to add tests for a different project, create a new folder at this level
    ├── __init__.py
    ├── allure_report
    ├── log
    ├── page    <-- Add new Page Objects here
    │   ├── __init__.py
    │   ├── category_page.py
    │   ├── home_page.py
    │   ├── search_page.py
    │   └── streamer_home_page.py
    ├── pytest.ini
    ├── screenshot
    └── testcase    <-- Store test cases according to different platforms
        ├── __init__.py
        ├── wap    <-- Test cases for WAP; if you want to add Android tests, create a new folder at this level
        │   ├── __init__.py
        │   ├── conftest.py    <-- Initialize different browser instances through different conftest settings
        │   └── test_twitch.py
        └── web
            ├── __init__.py
            ├── conftest.py
            └── test_twitch.py
```

---

# 自動化測試框架示範

## 介紹
![示範](doc/demo.gif)  
這是一個針對 WAP 測試自動化的示範專案。  
專案使用了 Selenium、WebDriver Manager、Pytest 和 Allure 等框架。  
設計時保留了對於 Android、iOS、WAP 和 WEB 測試的擴充性。  
測試結果將利用 Allure 報告保存，每個測試步驟結束後會進行截圖以方便除錯（可以選擇取消截圖以提高執行速度）。

## 執行測試
執行測試用例：
```
cd twitch

# 執行 WAP 測試
pytest -m wap_regression

# 執行 Web 測試
pytest -m web_regression
```

使用 Allure 開啟報告：
```
# 確保你的環境已安裝 Allure
# macOS
brew install allure

# 執行 allure server，在 html 上觀看 report
allure serve ./allure_report
```

## 專案擴充
1. 專案使用 PageObject 模式進行撰寫，你可以在 `{product_name}/page` 中新增頁面，例如 `twitch/page`。
2. 在每個 Page 中，`elements` 代表該頁面中可用來操作或定位的 DOM 元素，以字典形式記錄，並分為 web/android/ios 三類，方便在需要支援跨平台時重用 PageObject，而無需重寫。
3. 該 Page 上的操作將寫在該 Page 中，並在函數前使用 `allure.step` 記錄測試步驟。
4. 在 `{product_name}/testcase/{platform}` 中新增測試用例，例如 `twitch/testcase/wap`。

## 專案架構
```
.
├── README.md
├── common    <-- 共用元件
│   ├── __init__.py
│   ├── base_page.py
│   ├── browser.py
│   ├── decorator.py
│   └── platform.py
├── config    <-- 全局變數設定
│   └── __init__.py
├── doc    <-- README.md 使用的檔案
│   └── demo.gif
├── requirements.txt
└── twitch    <-- 專案目錄；若要新增不同專案的測試，可在此層新增資料夾
    ├── __init__.py
    ├── allure_report
    ├── log
    ├── page    <-- 在此新增新的 Page Object
    │   ├── __init__.py
    │   ├── category_page.py
    │   ├── home_page.py
    │   ├── search_page.py
    │   └── streamer_home_page.py
    ├── pytest.ini
    ├── screenshot
    └── testcase    <-- 按照不同平台存放測試用例
        ├── __init__.py
        ├── wap    <-- WAP 的測試用例；若要新增 Android 測試，則在同層新增資料夾
        │   ├── __init__.py
        │   ├── conftest.py    <-- 通過不同的 conftest 設定初始化不同的瀏覽器實例
        │   └── test_twitch.py
        └── web
            ├── __init__.py
            ├── conftest.py
            └── test_twitch.py
```