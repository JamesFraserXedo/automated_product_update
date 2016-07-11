import time
from selenium import webdriver
from selenium.webdriver.support.select import Select

from model.admin_page import AdminPage
from model.header import Header
from model.impersonate_page import ImpersonatePage
from model.live_product_list_page import LiveProductListPage
from model.login_page import LoginPage
from model.product_form import ProductForm
from product_types import ProductTypes
from StatusObject import StatusObject
from credentials import Credentials
from codec import *
from utils import Utils


class BaseUpdater:

    def __init__(self, customer_code):
        self.driver = None
        self.login_page = None
        self.admin_page = None
        self.impersonate_page = None
        self.header = None
        self.live_product_list_page = None
        self.product_form = None

        self.customer_code = customer_code

    def create_driver(self):
        self.driver = webdriver.Firefox()
        self.login_page = LoginPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.header = Header(self.driver)
        self.impersonate_page = ImpersonatePage(self.driver)
        self.live_product_list_page = LiveProductListPage(self.driver)
        self.product_form = ProductForm(self.driver)

    def impersonate(self):
        self.driver.get(Credentials.url)

        self.login_page.login(
            account_code=Credentials.account_code,
            user_name=Credentials.user_name,
            password=Credentials.password
        )

        self.admin_page.get_impersonate_button().click()

        self.impersonate_page.impersonate(self.customer_code)

    def update_product(self, product):
        status = OK
        messages = []

        self.header.get_live_products_button().click()

        self.live_product_list_page.filter_by_code(product.style)

        num_results = self.live_product_list_page.get_number_of_results(product.style)

        if num_results == 0:
            return self.handle_creation(product, messages)

        if num_results > 1:
            messages.append("More than one product with this code ({}) found".format(product.style))
            status = ERROR
            return StatusObject(status, messages)

        self.live_product_list_page.get_edit_product_button(product.style).click()

        if self.product_form.get_current_code() != product.style:
            messages.append("Attempted to update code {} , but accessed {} instead".format(product.style, self.product_form.get_current_code()))
            status = ERROR
            return StatusObject(status, messages)

        if self.product_form.get_current_collection() != product.collection:
            messages.append("Expected collection '{}' , but found '{}' instead".format(product.collection, self.product_form.get_current_collection()))
            status = WARNING
            return StatusObject(status, messages)

        if product.uk_size_range.replace(' ', '') not in self.product_form.get_current_size_range().replace(' ', ''):
            messages.append("Expected size range {} , but found {} instead".format(product.uk_size_range, self.product_form.get_current_size_range))
            status = WARNING
            return StatusObject(status, messages)

        current_uk_wholesale_price = self.product_form.get_current_price()
        if current_uk_wholesale_price != product.uk_wholesale_price:
            status = UPDATED
            self.product_form.get_price_inputbox().clear()
            self.product_form.price_inputbox().send_keys(str(round(product.uk_wholesale_price, 2)))
            messages.append("Updated price from £{} to £{}".format(round(current_uk_wholesale_price, 2), round(product.uk_wholesale_price, 2)))

        current_consumer_marketing_info = self.product_form.get_consumer_marketing_info_inputbox().text.replace('\r', ' ').replace('\n', ' ')
        current_retailer_marketing_info = self.product_form.get_retailer_marketing_info_inputbox().text.replace('\r', ' ').replace('\n', ' ')

        if product.marketing_info:
            if current_consumer_marketing_info == current_retailer_marketing_info == '':
                status = UPDATED
                self.product_form.get_consumer_marketing_info_inputbox().send_keys(product.marketing_info)
                messages.append("Added marketing info:")
                messages.append("\t{}".format(product.marketing_info))

            elif current_consumer_marketing_info != current_retailer_marketing_info:
                messages.append("Consumer and Retailer marketing info did not match before editing:")
                messages.append("\tConsumer: {}".format(current_consumer_marketing_info))
                messages.append("\tRetailer: {}".format(current_retailer_marketing_info))
                status = WARNING

            else:
                messages.append("Consumer and Retailer marketing already contain data:")
                messages.append("\t{}".format(current_consumer_marketing_info.replace('\r', ' ').replace('\n', ' ')))
                status = WARNING

        current_colours = self.product_form.get_current_colours()
        product_colours = [x.strip() for x in product.colours_available.split(',')]

        if sorted(current_colours) != sorted(product_colours):
            messages += self.product_form.update_colours(product_colours)
            status = UPDATED
            messages.append("Updated colours from {} to {}".format(current_colours, product_colours))
            # messages.append("Colours do not match:")
            # messages.append("\tExpected: {}".format(product_colours))
            # messages.append("\tActual: {}".format(current_colours))

        self.product_form.get_save_button().click()

        return StatusObject(status, messages)

    def handle_creation(self, product, messages):
        status = NEEDS_CREATED
        return StatusObject(status, messages)

        self.header.get_add_product_button().click()

        brand_select = Select(Utils.find_element_by_id_wait(self.driver, "BrandUnid"))
        brand_select.select_by_visible_text('Mori Lee')

        product_select = Select(Utils.find_element_by_id_wait(self.driver, "ProductTypeUnid"))
        if product.product_type == ProductTypes.MoriLee.BRIDESMAID_DRESS:
            product_select.select_by_visible_text('Bridesmaid Dress')
        elif product.product_type == ProductTypes.MoriLee.WEDDING_DRESS:
            product_select.select_by_visible_text('Wedding Dress')
        else:
            status = NEEDS_CREATED
            messages.append("Could not select product type {}".format(product.product_type))
            return StatusObject(status, messages)

        create_product_button = Utils.find_element_by_id_wait(self.driver, "CreateProductSingleButton")
        create_product_button.click()

        self.product_form.get_code_inputbox().send_keys(product.style)
        self.product_form.get_name_inputbox().send_keys(product.style)

        self.product_form.get_collection_select().select_by_visible_text(product.collection)

        # TODO
        self.product_form.get_leadtime_inputbox()

        self.product_form.get_price_inputbox().send_keys(str(round(product.uk_wholesale_price, 2)))

        # TODO
        self.product_form.get_rrp_inputbox()

        # TODO
        self.product_form.get_startdate_inputbox()

        if product.uk_size_range.replace(' ', '') == '18-30':
            self.product_page.get_size_range_select().select_by_visible_text('18-30 (Size: 18 -> 30)')
        elif product.uk_size_range.replace(' ', '') == '18-34':
            self.product_page.get_size_range_select().select_by_visible_text('18-34 (Size: 18 -> 34)')
        elif product.uk_size_range.replace(' ', '') == '4-26':
            self.product_page.get_size_range_select().select_by_visible_text('4-26 (Size: 4 -> 26)')
        elif product.uk_size_range.replace(' ', '') == '4-30':
            self.product_page.get_size_range_select().select_by_visible_text('4-30 (Size: 4 -> 30)')
        elif product.uk_size_range.replace(' ', '') == '6-24':
            self.product_page.get_size_range_select().select_by_visible_text('6-24 (Size: 6 -> 24)')
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
            self.product_form.get_consumer_marketing_info_inputbox().send_keys(product.marketing_info)
            self.product_form.get_retailer_marketing_info_inputbox().send_keys(product.marketing_info)

        quit()

        # self.product_form.get_save_button().click()

    def teardown(self):
        self.driver.quit()
