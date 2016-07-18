from model.locators import Locators
from model.object.base_page_element import *


class ImpersonateButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.AdminPage.impersonate_button
        )


class AdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.impersonate_button = ImpersonateButton(driver)

