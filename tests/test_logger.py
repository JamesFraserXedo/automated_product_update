from selenium import webdriver

import Utils
from logger import Logger

def test_logger():
    logger = Logger('test')

    try:
        a = 1 / 0
    except Exception as e:
        logger.error(e)


def test_screenshot():
    driver = webdriver.Firefox()
    driver.get('https://www.google.com')
    Utils.screenshot(driver)
    driver.quit()

test_screenshot()