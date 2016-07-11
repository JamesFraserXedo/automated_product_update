from utils import Utils


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def get_account_code_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "AccountCode")

    def get_user_name_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "UserName")

    def get_password_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "Password")

    def get_login_button(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//*[@class='commonButton inputButton']")

    def login(self, account_code, user_name, password):
        self.get_account_code_inputbox().send_keys(account_code)
        self.get_user_name_inputbox().send_keys(user_name)
        self.get_password_inputbox().send_keys(password)
        self.get_login_button().click()