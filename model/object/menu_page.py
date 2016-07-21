from model.locators import Locators
from model.object.base_page_object import BasePageObject


class MenuPage(BasePageObject):
    def __init__(self, driver):
        super().__init__(driver, Locators.MenuPage.product_setup_panel)