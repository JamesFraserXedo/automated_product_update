from selenium.webdriver.support.select import Select

import Utils


class BasePageElement(object):

    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return Utils.find_element_wait(self.driver, self.locator)

    @property
    def text(self):
        return self.element.text

    def send_keys(self, keys):
        self.element.clear()
        self.element.send_keys(keys)


class Button(BasePageElement):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    def click(self):
        self.element.click()


class Inputbox(BasePageElement):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @BasePageElement.text.setter
    def text(self, value):
        self.send_keys(value)


class Selector(BasePageElement):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def selector(self):
        return Select(self.element)

    @property
    def selected(self):
        return self.selector.first_selected_option.text

    @property
    def options(self):
        return (o.text for o in self.selector.options)

    @selected.setter
    def selected(self, value):
        return self.selector.select_by_visible_text(value)

    def select_by_partial_text(self, text):
        return self.element.find_element_by_xpath("//option[contains(text(), '{}')]".format(text)).click()


class Checkbox(BasePageElement):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)

    @property
    def selected(self):
        return self.element.is_selected()

    def select(self):
        if not self.selected:
            self.element.click()

    def deselect(self):
        if self.selected:
            self.element.click()