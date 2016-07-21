import time
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from model.locators import Locators
from model.object.elements import *
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


class DraftProductsListPage(BasePageObject):
    def __init__(self, driver):
        super().__init__(driver, Locators.DraftProductsListPage.delete_draft_product_label)
        self.code_filter_button = CodeFilterButton(driver)
        self.filter_inputbox = FilterInputbox(driver)
        self.activate_filter_button = ActivateFilterButton(driver)

    def open_code_filter_panel(self):
        if not Utils.element_exists(self.driver, Locators.LiveProductListPage.filter_inputbox):
            self.code_filter_button.click()
            time.sleep(1)

    def filter_by_code(self, code):
        self.open_code_filter_panel()
        self.filter_inputbox.text = code
        self.filter_inputbox.submit()

        # self.open_code_filter_panel()
        # self.activate_filter_button.click()
        time.sleep(1)

        if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
            Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
            if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                    Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                    if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                        raise Exception('Could not sort list')

    def number_of_results(self, code):
        self.filter_by_code(code)
        return len(self.driver.find_elements_by_xpath("//tr[@role='row']/td[text()='{}']/..//input[@value='Delete']".format(code)))

    def delete_draft(self, code):
        before_text = Utils.find_element_by_xpath_wait(self.driver, "//*[@id='topPager']/span").text
        Utils.find_element_by_xpath_wait(self.driver, "//tr[@role='row']/td[text()='{}']/..//input[@value='Delete']".format(code)).click()
        time.sleep(1)
        alert = self.driver.switch_to_alert()
        alert.accept()

        while Utils.find_element_by_xpath_wait(self.driver, "//*[@id='topPager']/span", timeout=120).text == before_text:
            pass
