import time

from utils import Utils


class LiveProductListPage:

    def __init__(self, driver):
        self.driver = driver

    def get_add_product_button(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Add Product']")

    def filter_by_code(self, code):
        code_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@data-title='Code']//span[@class='k-icon k-filter']")
        code_filter_button.click()

        filter_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[@class='k-textbox']")
        filter_inputbox.send_keys(code)

        activate_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//button[@type='submit']")
        activate_filter_button.click()

        time.sleep(1)

        if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
            Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
            if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                if (len(self.driver.find_elements_by_xpath(
                        "//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                    Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                    if (len(self.driver.find_elements_by_xpath(
                            "//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                        raise Exception('Could not sort list')

    def get_number_of_results(self, code):
        return len(self.driver.find_elements_by_xpath("//tr[@role='row']/td[text()='{}']/..//input[@title='Edit']".format(code)))

    def get_edit_product_button(self, code):
        return Utils.find_element_by_xpath_wait(self.driver, "//tr[@role='row']/td[text()='{}']/..//input[@title='Edit']".format(code))