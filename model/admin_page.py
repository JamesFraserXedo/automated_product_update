from utils import Utils


class AdminPage:

    def __init__(self, driver):
        self.driver = driver

    def get_impersonate_button(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//a[@title='Impersonate']/..")

