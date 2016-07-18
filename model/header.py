from model.locators import Locators
from model.object.base_page_element import *
from model.object.base_page_object import BasePageObject


class AddProductButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.Header.add_product_button
        )


class LiveProductsButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.Header.live_products_button
        )


class Header(BasePageObject):
    def __init__(self, driver):
        self.driver = driver
        self.add_product_button = AddProductButton(driver)
        self.live_products_button = LiveProductsButton(driver)


