import os

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import *


def scroll_to_element(driver, element):
    # driver.execute_script("return arguments[0].scrollIntoView();", element)
    driver.execute_script("window.scrollTo(" + str(element.location['x']) + "," + str(element.location['y'] - 400) + ");")


def find_element_by_xpath_wait(driver, loc, timeout=30):
    wait = WebDriverWait(
        driver,
        timeout,
        poll_frequency=1,
        ignored_exceptions=[
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )
    element = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, loc)))
    scroll_to_element(driver, element)
    return element


def find_element_by_id_wait(driver, loc, timeout=30):
    wait = WebDriverWait(
        driver,
        timeout,
        poll_frequency=1,
        ignored_exceptions=[
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )
    element = wait.until(expected_conditions.element_to_be_clickable((By.ID, loc)))
    scroll_to_element(driver, element)
    return element


def find_element_wait(driver, by, timeout=30):
    wait = WebDriverWait(
        driver,
        timeout,
        poll_frequency=1,
        ignored_exceptions=[
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )

    element = wait.until(expected_conditions.element_to_be_clickable(by))
    scroll_to_element(driver, element)
    return element


def find_elements_by(driver, by):
    if by[0] == By.XPATH:
        return driver.find_elements_by_xpath(by[1])
    if by[0] == By.ID:
        return driver.find_elements_by_css_selector("[id='{}']".format(by[1]))

    raise ValueError("Could not use other locator")


def element_exists(driver, by):
    elements = find_elements_by(driver, by)
    if len(elements) > 0:
        return elements[0].is_displayed()
    return False


def screenshot(driver, id=None):
    base_dir = os.path.dirname(__file__)
    if id:
        prefix = id + '_'
    else:
        prefix = ''
    name = os.path.join(base_dir, "screenshots/{}{}.png".format(prefix, time.strftime('%Y-%m-%d_%H-%M-%S')))
    driver.save_screenshot(name)
    return name
