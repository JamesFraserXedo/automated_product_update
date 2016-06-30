# import time
# from selenium import webdriver
# from selenium.webdriver.support.select import Select
#
# from utils import Utils
#
#
# class MainUpdater:
#
#     def __init__(self, customer_code):
#         self.driver = None
#         self.customer_code = customer_code
#
#     def create_driver(self):
#         self.driver = webdriver.Firefox()
#         self.driver.get("https://oc.xedosoftware.com/Xedo/All/Admin/Info")
#
#         account_code_inputbox = Utils.find_element_by_id_wait(self.driver, "AccountCode")
#         user_name_inputbox = Utils.find_element_by_id_wait(self.driver, "UserName")
#         password_inputbox = Utils.find_element_by_id_wait(self.driver, "Password")
#         login_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@class='commonButton inputButton']")
#
#         account_code_inputbox.send_keys('xedoadmin')
#         user_name_inputbox.send_keys('administrator')
#         password_inputbox.send_keys('a1s2d3f4g5x')
#         login_button.click()
#
#         # time.sleep(1)
#
#         impersonate_button = Utils.find_element_by_xpath_wait(self.driver, "//a[@title='Impersonate']/..")
#         impersonate_button.click()
#         # time.sleep(2)
#
#     def impersonate(self):
#         customer_code_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//*[@class='custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left ui-autocomplete-input']")
#         customer_code_inputbox.send_keys(customer_code)
#
#         first_result = Utils.find_element_by_xpath_wait(self.driver, "//*[@id='ui-id-1']/li")
#         first_result.click()
#
#         select_retailer_button = Utils.find_element_by_id_wait(self.driver, "select-retailer")
#         select_retailer_button.click()
#
#         # time.sleep(1)
#
#         impersonate_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@class='btnLogin button']")
#         impersonate_button.click()
#
#     def update_product(self, product):
#         status = 1
#         messages = []
#
#         live_products_button = Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Live Products']")
#         live_products_button.click()
#
#         # time.sleep(2)
#
#         code_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@data-title='Code']//span[@class='k-icon k-filter']")
#         code_filter_button.click()
#
#         # time.sleep(1)
#
#         filter_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[@class='k-textbox']")
#         filter_inputbox.send_keys(product.style)
#
#         activate_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//button[@type='submit']")
#         activate_filter_button.click()
#
#         time.sleep(1)
#
#         product_codes = self.driver.find_elements_by_xpath("//tr[@role='row']/td[2]")
#         if len(product_codes) == 0:
#             messages.append("\tThis product needs created".format(product.style))
#             return {
#                 "status": 0,
#                 "messages": messages
#             }
#
#         if len(product_codes) > 1:
#             count = 0
#             for product_code in product_codes:
#                 if product_code.text == product.style:
#                     count += 1
#
#             if count > 1:
#                 messages.append("\tMore than one product with this code ({}) found".format(product.style))
#                 return {
#                     "status": -1,
#                     "messages": messages
#                 }
#
#         edit_product_button = Utils.find_element_by_xpath_wait(self.driver, "//input[@title='Edit']")
#         edit_product_button.click()
#         # time.sleep(5)
#
#         current_code_label = Utils.find_element_by_id_wait(self.driver, "StagedProduct_Code")
#         current_code = current_code_label.get_attribute("value")
#         if current_code != product.style:
#             messages.append("\tAttempted to update code {} , but accessed {} instead".format(product.style, current_code))
#             return {
#                 "status": -1,
#                 "messages": messages
#             }
#
#         size_range_select = Select(Utils.find_element_by_xpath_wait(self.driver, "//*[@class='size-templates-ddl']"))
#         current_size_range = size_range_select.first_selected_option.text
#         if product.uk_size_range.replace(' ', '') not in current_size_range.replace(' ', ''):
#             messages.append("\tExpected size range {} , but found {} instead".format(product.uk_size_range, current_size_range))
#             return {
#                 "status": 0,
#                 "messages": messages
#             }
#
#         price_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'CostPrice')]")
#         current_uk_wholesale_price = float(price_inputbox.get_attribute("value"))
#         if current_uk_wholesale_price != product.uk_wholesale_price:
#             status = 2
#             price_inputbox.clear()
#             price_inputbox.send_keys(str(round(product.uk_wholesale_price, 2)))
#             messages.append("\tUpdated price from £{} to £{}".format(round(current_uk_wholesale_price, 2), round(product.uk_wholesale_price, 2)))
#
#         consumer_marketing_info_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_ConsumerMarketingInfo")
#         retailer_marketing_info_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_MarketingInfo")
#
#         current_consumer_marketing_info = consumer_marketing_info_inputbox.text
#         current_retailer_marketing_info = retailer_marketing_info_inputbox.text
#
#         if product.marketing_info:
#             if current_consumer_marketing_info == current_retailer_marketing_info == '':
#                 status = 2
#                 consumer_marketing_info_inputbox.send_keys(product.marketing_info)
#                 messages.append("Added marketing info:")
#                 messages.append("\t{}".format(product.marketing_info))
#
#             elif current_consumer_marketing_info != current_retailer_marketing_info:
#                 messages.append("Consumer and Retailer marketing info did not match before editing".format(product.uk_size_range, current_size_range))
#                 status = 0
#
#             else:
#                 messages.append("Consumer and Retailer marketing already contain data:")
#                 messages.append("\t{}".format(current_consumer_marketing_info.replace('\r', '').replace('\n', '')))
#                 status = 0
#
#         save_button = Utils.find_element_by_id_wait(self.driver, "SaveProduct")
#         save_button.click()
#         # time.sleep(1)
#
#         return {
#             "status": status,
#             "messages": messages
#         }
#
#     def teardown(self):
#         self.driver.quit()
