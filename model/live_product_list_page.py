from model.locators import Locators
from model.object.base_page_element import *
from model.object.base_page_object import BasePageObject
import Utils


class CodeFilterButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LiveProductListPage.code_filter_button
        )


class FilterInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LiveProductListPage.filter_inputbox
        )


class ActivateFilterButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LiveProductListPage.activate_filter_button
        )


class LiveProductsListPage(BasePageObject):
    def __init__(self, driver):
        self.driver = driver
        self.code_filter_button = CodeFilterButton(driver)
        self.filter_inputbox = FilterInputbox(driver)
        self.activate_filter_button = ActivateFilterButton(driver)

    def filter_by_code(self, code):
        code_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@data-title='Code']//span[@class='k-icon k-filter']")
        code_filter_button.click()

        filter_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[@class='k-textbox']")
        filter_inputbox.text =code

        activate_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//button[@type='submit']")
        activate_filter_button.click()

        if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
            Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
            if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                    Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                    if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                        raise Exception('Could not sort list')

    def number_of_results(self, code):
        return len(self.driver.find_elements_by_xpath("//tr[@role='row']/td[text()='{}']/..//input[@title='Edit']".format(code)))

    def edit_product_button(self, code):
        Utils.find_element_by_xpath_wait(self.driver, "//tr[@role='row']/td[text()='{}']/..//input[@title='Edit']".format(code)).click()
