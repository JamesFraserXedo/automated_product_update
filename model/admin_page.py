from model.locators import Locators
from model.object.base_page_object import BasePageObject
from model.object.elements import *


class ImpersonateButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.AdminPage.impersonate_button
        )


class AdminPage(BasePageObject):
    def __init__(self, driver):
        super().__init__(driver, Locators.AdminPage.impersonate_button)
        self.impersonate_button = ImpersonateButton(driver)

