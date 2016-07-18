from model.locators import *
from utils import Utils


class BasePage:

    def find_element(self, driver, by, loc):
        if by == ID:
            return Utils.find_element_by_id_wait(driver, loc)
        elif by == XPATH:
            return Utils.find_element_by_xpath_wait(driver, loc)
        else:
            return None