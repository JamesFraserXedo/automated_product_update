from model.locators import Locators
from model.object.elements import *
from model.object.base_page_object import BasePageObject


class AccountCodeInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LoginPage.account_code_inputbox
        )


class UserNameInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LoginPage.user_name_inputbox
        )


class PasswordInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LoginPage.password_inputbox
        )


class LoginButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.LoginPage.login_button
        )


class LoginPage(BasePageObject):
    def __init__(self, driver):
        self.driver = driver
        self.account_code_inputbox = AccountCodeInputbox(driver)
        self.user_name_inputbox = UserNameInputbox(driver)
        self.password_inputbox = PasswordInputbox(driver)
        self.login_button = LoginButton(driver)

    def login(self, account_code, user_name, password):
        self.account_code_inputbox.text = account_code
        self.user_name_inputbox.text = user_name
        self.password_inputbox.text = password
        self.login_button.click()