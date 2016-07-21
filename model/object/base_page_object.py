import unittest
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import Utils


class BasePageObject(unittest.TestCase):
    def __init__(self, driver, load_element_locator):
        self.driver = driver
        self.load_element_locator = load_element_locator

    def wait_until_on_page(self, timeout=90):
        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=1,
            ignored_exceptions=[
                ElementNotVisibleException
            ]
        )

        wait.until(expected_conditions.visibility_of_element_located(self.load_element_locator))

    @property
    def on_page(self):
        return len(Utils.find_elements_by(self.driver, self.load_element_locator)) > 0