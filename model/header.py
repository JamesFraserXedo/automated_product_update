from utils import Utils


class Header:

    def __init__(self, driver):
        self.driver = driver

    def get_add_product_button(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Add Product']")

    def get_live_products_button(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Live Products']")

