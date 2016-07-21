from model.locators import Locators
from model.object.elements import *
from model.object.base_page_object import BasePageObject
import Utils


class CustomerCodeInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ImpersonatePage.customer_code_inputbox
        )


class SelectRetailerButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ImpersonatePage.select_retailer_button
        )


class ImpersonateButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ImpersonatePage.impersonate_button
        )


class ImpersonatePage(BasePageObject):
    def __init__(self, driver):
        super().__init__(driver, Locators.ImpersonatePage.customer_code_inputbox)
        self.customer_code_inputbox = CustomerCodeInputbox(driver)
        self.select_retailer_button = SelectRetailerButton(driver)
        self.impersonate_button = ImpersonateButton(driver)

    def impersonate(self, alias):
        self.customer_code_inputbox.text = alias
        Utils.find_element_wait(self.driver, Locators.ImpersonatePage.first_result).click()
        self.select_retailer_button.click()
        self.impersonate_button.click()


