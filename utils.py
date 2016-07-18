from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import *


def scroll_to_element(driver, element):
    driver.execute_script("return arguments[0].scrollIntoView();", element)


def find_element_by_xpath_wait(driver, loc):
    wait = WebDriverWait(
        driver,
        30,
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
