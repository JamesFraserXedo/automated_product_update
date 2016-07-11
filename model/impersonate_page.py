from utils import Utils


class ImpersonatePage:

    def __init__(self, driver):
        self.driver = driver

    def get_customer_code_inputbox(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//*[@class='custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left ui-autocomplete-input']")

    def get_select_retailer_button(self):
        return Utils.find_element_by_id_wait(self.driver, "select-retailer")

    def get_impersonate_button(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//*[@class='btnLogin button']")

    def impersonate(self, alias):
        self.get_customer_code_inputbox().send_keys(alias)
        first_result = Utils.find_element_by_xpath_wait(self.driver, "//*[@id='ui-id-1']/li")
        first_result.click()
        self.get_select_retailer_button().click()
        self.get_impersonate_button().click()


