import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TWITCH_PIC_DIR = os.path.join(BASE_DIR, 'twitch', "screenshot")
TWITCH_LOG_DIR = os.path.join(BASE_DIR, 'twitch', "log")

WEB_BROWSER_NAME = "Chrome"  # choose browser if supported
WEB_IMPLICITLY_WAIT_TIME = 15  # selenium implicitly_wait in second
WEB_POLL_FREQUENCY = 0.2  # selenium poll_frequency in second

APP_IMPLICITLY_WAIT_TIME = 10    # appium implicitly_wait in second

## android
# ANDROID_CAPA:

## iOS
# IOS_CAPA: