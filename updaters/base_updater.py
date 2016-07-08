import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from product_types import ProductTypes
from StatusObject import StatusObject
from credentials import Credentials
from codec import *
from utils import Utils


class BaseUpdater:

    def __init__(self, customer_code):
        self.driver = None
        self.customer_code = customer_code

    def create_driver(self):
        self.driver = webdriver.Firefox()

    def impersonate(self):
        self.driver.get(Credentials.url)

        account_code_inputbox = Utils.find_element_by_id_wait(self.driver, "AccountCode")
        user_name_inputbox = Utils.find_element_by_id_wait(self.driver, "UserName")
        password_inputbox = Utils.find_element_by_id_wait(self.driver, "Password")
        login_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@class='commonButton inputButton']")

        account_code_inputbox.send_keys(Credentials.account_code)
        user_name_inputbox.send_keys(Credentials.user_name)
        password_inputbox.send_keys(Credentials.password)
        login_button.click()

        impersonate_link = Utils.find_element_by_xpath_wait(self.driver, "//a[@title='Impersonate']/..")
        impersonate_link.click()

        customer_code_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//*[@class='custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left ui-autocomplete-input']")
        customer_code_inputbox.send_keys(self.customer_code)

        first_result = Utils.find_element_by_xpath_wait(self.driver, "//*[@id='ui-id-1']/li")
        first_result.click()

        select_retailer_button = Utils.find_element_by_id_wait(self.driver, "select-retailer")
        select_retailer_button.click()

        impersonate_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@class='btnLogin button']")
        impersonate_button.click()

    def update_product(self, product):
        status = OK
        messages = []

        live_products_button = Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Live Products']")
        live_products_button.click()

        code_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//*[@data-title='Code']//span[@class='k-icon k-filter']")
        code_filter_button.click()

        filter_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[@class='k-textbox']")
        filter_inputbox.send_keys(product.style)

        activate_filter_button = Utils.find_element_by_xpath_wait(self.driver, "//button[@type='submit']")
        activate_filter_button.click()

        time.sleep(1)

        if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
            Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
            if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                    Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Code']").click()
                    if (len(self.driver.find_elements_by_xpath("//*[@data-title='Code']//*[@class='k-icon k-i-arrow-n']"))) == 0:
                        raise Exception('Could not sort list')

        product_codes = self.driver.find_elements_by_xpath("//tr[@role='row']/td[text()='{}']/..//input[@title='Edit']".format(product.style))
        if len(product_codes) == 0:
            return self.handle_creation(product, messages)

        if len(product_codes) > 1:
            messages.append("\tMore than one product with this code ({}) found".format(product.style))
            status = ERROR
            return StatusObject(status, messages)

        edit_product_button = Utils.find_element_by_xpath_wait(self.driver, "//tr[@role='row']/td[text()='{}']/..//input[@title='Edit']".format(product.style))
        edit_product_button.click()

        current_code_label = Utils.find_element_by_id_wait(self.driver, "StagedProduct_Code")
        current_code = current_code_label.get_attribute("value")
        if current_code != product.style:
            messages.append("\tAttempted to update code {} , but accessed {} instead".format(product.style, current_code))
            status = ERROR
            return StatusObject(status, messages)

        collection_select = Select(Utils.find_element_by_id_wait(self.driver, "CollectionUnid"))
        current_collection_text = collection_select.first_selected_option.text
        if current_collection_text != product.collection:
            messages.append("\tExpected collection '{}' , but found '{}' instead".format(product.collection, current_collection_text))
            status = WARNING
            return StatusObject(status, messages)

        size_range_select = Select(Utils.find_element_by_xpath_wait(self.driver, "//*[@class='size-templates-ddl']"))
        current_size_range = size_range_select.first_selected_option.text
        if product.uk_size_range.replace(' ', '') not in current_size_range.replace(' ', ''):
            messages.append("\tExpected size range {} , but found {} instead".format(product.uk_size_range, current_size_range))
            status = WARNING
            return StatusObject(status, messages)

        price_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'CostPrice')]")
        current_uk_wholesale_price = float(price_inputbox.get_attribute("value"))
        if current_uk_wholesale_price != product.uk_wholesale_price:
            status = UPDATED
            price_inputbox.clear()
            price_inputbox.send_keys(str(round(product.uk_wholesale_price, 2)))
            messages.append("\tUpdated price from £{} to £{}".format(round(current_uk_wholesale_price, 2), round(product.uk_wholesale_price, 2)))

        consumer_marketing_info_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_ConsumerMarketingInfo")
        retailer_marketing_info_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_MarketingInfo")

        current_consumer_marketing_info = consumer_marketing_info_inputbox.text
        current_retailer_marketing_info = retailer_marketing_info_inputbox.text

        if product.marketing_info:
            if current_consumer_marketing_info == current_retailer_marketing_info == '':
                status = UPDATED
                consumer_marketing_info_inputbox.send_keys(product.marketing_info)
                messages.append("Added marketing info:")
                messages.append("\t{}".format(product.marketing_info))

            elif current_consumer_marketing_info != current_retailer_marketing_info:
                messages.append("Consumer and Retailer marketing info did not match before editing:")
                messages.append("\t{}".format(current_consumer_marketing_info))
                messages.append("\t{}".format(current_retailer_marketing_info))
                status = WARNING

            else:
                messages.append("Consumer and Retailer marketing already contain data:")
                messages.append("\t{}".format(current_consumer_marketing_info.replace('\r', '').replace('\n', '')))
                status = WARNING

        save_button = Utils.find_element_by_id_wait(self.driver, "SaveProduct")
        save_button.click()

        return StatusObject(status, messages)

    def handle_creation(self, product, messages):
        add_product_button = Utils.find_element_by_xpath_wait(self.driver, "//a[text()='Add Product']")
        add_product_button.click()

        brand_select = Select(Utils.find_element_by_id_wait(self.driver, "BrandUnid"))
        brand_select.select_by_visible_text('Mori Lee')

        product_select = Select(Utils.find_element_by_id_wait(self.driver, "ProductTypeUnid"))
        if product.product_type == ProductTypes.MoriLee.BRIDESMAID_DRESS:
            product_select.select_by_visible_text('Bridesmaid Dress')
        elif product.product_type == ProductTypes.MoriLee.WEDDING_DRESS:
            product_select.select_by_visible_text('Wedding Dress')
        else:
            print("No recognise product type {}".format(product.product_type))
            status = NEEDS_CREATED
            messages.append("Could not select product type {}".format(product.product_type))
            return StatusObject(status, messages)

        create_product_button = Utils.find_element_by_id_wait(self.driver, "CreateProductSingleButton")
        create_product_button.click()

        code_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_Code")
        code_inputbox.send_keys(product.style)
        name_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_Caption")
        name_inputbox.send_keys(product.style)

        collection_select = Select(Utils.find_element_by_id_wait(self.driver, "CollectionUnid"))
        collection_select.select_by_visible_text(product.collection)

        # TODO
        leadtime_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'LeadTime')]")

        price_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'CostPrice')]")
        price_inputbox.send_keys(str(round(product.uk_wholesale_price, 2)))

        # TODO
        rrp_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'Rrp')]")

        # TODO
        startdate_inputbox = Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'StartDatepicker')]")

        size_range_select = Select(Utils.find_element_by_xpath_wait(self.driver, "//*[@class='size-templates-ddl']"))
        if product.uk_size_range.replace(' ', '') == '18-30':
            size_range_select.select_by_visible_text('18-30 (Size: 18 -> 30)')
        elif product.uk_size_range.replace(' ', '') == '18-34':
            size_range_select.select_by_visible_text('18-34 (Size: 18 -> 34)')
        elif product.uk_size_range.replace(' ', '') == '4-26':
            size_range_select.select_by_visible_text('4-26 (Size: 4 -> 26)')
        elif product.uk_size_range.replace(' ', '') == '4-30':
            size_range_select.select_by_visible_text('4-30 (Size: 4 -> 30)')
        elif product.uk_size_range.replace(' ', '') == '6-24':
            size_range_select.select_by_visible_text('6-24 (Size: 6 -> 24)')
        else:
            status = NEEDS_CREATED
            messages.append("Could not select size {}".format(product.uk_size_range))
            return StatusObject(status, messages)

        edit_colours_button = Utils.find_element_by_id_wait(self.driver, "EditColours")
        edit_colours_button.click()

        for colour in product.colours_available.split(','):
            colour = colour.strip()

            try:
                colour_select = Select(Utils.find_element_by_id_wait(self.driver, "AvailableIds"))
                colour_select.select_by_visible_text(colour)

                select_highlighted_button = Utils.find_element_by_id_wait(self.driver, "SelectHighlighted")
                select_highlighted_button.click()
            except:
                messages.append("Could not add colour {}".format(colour))

        update_close_button = Utils.find_element_by_id_wait(self.driver, "SaveDialog")
        update_close_button.click()

        if product.marketing_info:
            consumer_marketing_info_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_ConsumerMarketingInfo")
            retailer_marketing_info_inputbox = Utils.find_element_by_id_wait(self.driver, "StagedProduct_MarketingInfo")

            consumer_marketing_info_inputbox.send_keys(product.marketing_info)
            retailer_marketing_info_inputbox.send_keys(product.marketing_info)

        quit()

        save_product_button = Utils.find_element_by_id_wait(self.driver, "SaveProduct")
        # save_product_button.click()

    def teardown(self):
        self.driver.quit()
