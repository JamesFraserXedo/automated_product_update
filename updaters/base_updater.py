import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from Tools import *
from model.admin_page import AdminPage
from model.colour_palette import ColourPalette
from model.edit_product_page import EditProductPage
from model.header import Header
from model.impersonate_page import ImpersonatePage
from model.live_product_list_page import LiveProductsListPage
from model.login_page import LoginPage
from product_types import ProductTypes
from StatusObject import StatusObject
from credentials import Credentials
from codec import *
import Utils

RRP_MULTIPLIER = 2.75


class BaseUpdater:

    def __init__(self, customer_code):
        self.driver = webdriver.Firefox()
        self.login_page = LoginPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.header = Header(self.driver)
        self.impersonate_page = ImpersonatePage(self.driver)
        self.live_product_list_page = LiveProductsListPage(self.driver)
        self.product_page = EditProductPage(self.driver)
        self.colour_palette = ColourPalette(self.driver)
        self.customer_code = customer_code
        self.messages = None
        self.status_object = None

    def impersonate(self):
        self.driver.get(Credentials.url)

        self.login_page.login(
            account_code=Credentials.account_code,
            user_name=Credentials.user_name,
            password=Credentials.password
        )

        self.admin_page.impersonate_button.click()

        self.impersonate_page.impersonate(self.customer_code)

    def update_product(self, product):
        self.messages = []
        self.status_object = StatusObject(code=product.style)

        num_results = self.num_of_products(product)

        if num_results == 0:
            self.handle_creation(product)
        elif num_results > 1:
            self.status_object.add_message("More than one product with this code ({}) found".format(product.style))
            self.status_object.status = ERROR
        else:
            self.live_product_list_page.edit_product_button(product.style).click()

            self.check_code(product)
            self.check_collection(product)
            self.check_size_range(product)
            self.check_price(product)
            self.check_rrp(product)
            self.check_marketing_info(product)
            self.check_colours(product)

            if self.status_object.status == ERROR:
                self.product_page.cancel_button.click()
            else:
                self.product_page.save_button.click()

        return self.status_object

    def handle_creation(self, product):
        self.header.add_product_button.click()

        brand_select = Select(Utils.find_element_by_id_wait(self.driver, "BrandUnid"))
        brand_select.select_by_visible_text('Mori Lee')

        product_select = Select(Utils.find_element_by_id_wait(self.driver, "ProductTypeUnid"))
        if product.product_type == ProductTypes.MoriLee.BRIDESMAID_DRESS:
            product_select.select_by_visible_text('Bridesmaid Dress')
        elif product.product_type == ProductTypes.MoriLee.WEDDING_DRESS:
            product_select.select_by_visible_text('Wedding Dress')
        else:
            self.status_object.status = CREATED
            self.status_object.add_message("Could not select product type {}".format(product.product_type))
            return self.status_object

        create_product_button = Utils.find_element_by_id_wait(self.driver, "CreateProductSingleButton")
        create_product_button.click()

        self.product_page.code_inputbox.text = product.style

        self.product_page.name_inputbox.text = product.style
        self.status_object.new_name = self.product_page.name_inputbox.text

        self.product_page.collection_select.selected = product.collection
        self.status_object.new_collection = self.product_page.collection_select.selected

        path_to_image, all_images = get_path_to_image(product.style)
        if path_to_image:
            self.product_page.image_uploader.text = path_to_image
            self.status_object.new_image = self.product_page.image_uploader.text
            self.status_object.all_images = all_images
        else:
            self.status_object.new_image = None
            self.status_object.all_images = None

        self.product_page.price_inputbox.text = str(round(product.uk_wholesale_price, 0))
        self.status_object.new_price = self.product_page.price_inputbox.text

        self.product_page.rrp_inputbox.text = str(round(product.uk_wholesale_price * RRP_MULTIPLIER, 0))
        self.status_object.new_rrp = self.product_page.rrp_inputbox.text

        self.product_page.set_size_range(product.size_lower, product.size_upper)
        if product.colours_available:
            self.product_page.edit_colours_button.click()
            messages = self.colour_palette.update_colours(product.colours_available)
            self.status_object.new_colours = self.product_page.current_colours
        elif product.colour_set:
            self.product_page.edit_colours_button.click()
            messages = self.colour_palette.update_colour_set(product.colour_set)
            self.status_object.new_colours = self.product_page.current_colour_set

        if len(messages) > 0:
            self.status_object.status = ERROR
            self.status_object.add_message(messages)

        if product.marketing_info:
            self.product_page.append_consumer_marketing_info(product.marketing_info)
            self.product_page.append_retailer_marketing_info(product.marketing_info)

            if 'Available in 3 lengths - standard 61", 58" & 55"' in product.marketing_info:
                self.product_page.expand_all_options_button.click()
                time.sleep(1)
                self.product_page.special_length_option_checkbox.select()
                self.status_object.new_features = "Special Lengths"

        self.status_object.status = CREATED

        if self.status_object.status == ERROR:
            self.product_page.cancel_button.click()
        else:
            self.product_page.save_button.click()

    def teardown(self):
        self.driver.quit()
        pass

    def num_of_products(self, product):
        self.header.live_products_button.click()
        self.live_product_list_page.filter_by_code(product.style)
        return self.live_product_list_page.number_of_results(product.style)

    def check_code(self, product):
        if self.status_object.status == ERROR:
            return
        if self.product_page.code_inputbox.text != product.style:
            self.status_object.add_message("Attempted to update code {} , but accessed {} instead".format(product.style,
                                                                                           self.product_page.code_inputbox.text))
            self.status_object.status = ERROR

    def check_collection(self, product):
        if self.status_object.status == ERROR:
            return
        if self.product_page.collection_select.selected != product.collection:
            self.status_object.add_message("Expected collection '{}' , but found '{}' instead".format(product.collection,
                                                                                       self.product_page.collection_select.selected))
            self.status_object.status = ERROR

    def check_size_range(self, product):
        if self.status_object.status == ERROR:
            return
        if product.uk_size_range.replace(' ', '') not in self.product_page.size_range_select.options:
            self.status_object.add_message("Expected size range {} , but found {} instead".format(product.uk_size_range,
                                                                                   self.product_page.size_range_select.selected))
            self.status_object.status = ERROR

    def check_price(self, product):
        if self.status_object.status == ERROR:
            return
        current_uk_wholesale_price = self.product_page.price_inputbox.text
        if current_uk_wholesale_price != product.uk_wholesale_price:
            self.status_object.status = UPDATED
            self.product_page.price_inputbox.send_keys(str(round(product.uk_wholesale_price, 0)))
            self.status_object.old_price = current_uk_wholesale_price
            self.status_object.new_price = product.uk_wholesale_price

    def check_rrp(self, product):
        if self.status_object.status == ERROR:
            return

        current_rrp = self.product_page.rrp_inputbox.text
        expected_rrp = str(round(product.uk_wholesale_price * RRP_MULTIPLIER, 0))

        if current_rrp != expected_rrp:
            self.status_object.status = UPDATED
            self.product_page.rrp_inputbox.text = expected_rrp

            self.status_object.old_rrp = current_rrp
            self.status_object.new_rrp = expected_rrp

    def check_marketing_info(self, product):
        if self.status_object.status == ERROR:
            return
        if product.marketing_info:
            self.product_page.append_consumer_marketing_info(product.marketing_info, self.status_object)
            self.product_page.append_retailer_marketing_info(product.marketing_info, self.status_object)

            if 'Available in 3 lengths - standard 61", 58" & 55"' in product.marketing_info:
                self.product_page.expand_all_options_button.click()
                time.sleep(1)
                if not self.product_page.special_length_option_checkbox.selected:
                    self.product_page.special_length_option_checkbox.select()
                    self.status_object.old_features = "None"
                    self.status_object.new_features = "Special Lengths"

    def check_colours(self, product):
        if self.status_object.status == ERROR:
            return
        if product.colours_available:
            current_colours = self.product_page.current_colours
            product_colours = [x.strip() for x in product.colours_available.split(',')]

            if sorted(current_colours) != sorted(product_colours):

                colour_messages = self.product_page.update_colours(product_colours)
                if len(colour_messages) == 0:
                    self.status_object.status = UPDATED
                else:
                    self.status_object.status = WARNING

                self.messages += colour_messages
                old_colours = current_colours
                current_colours = self.product_page.current_colours
                if old_colours != current_colours:
                    self.status_object.old_colours = old_colours
                    self.status_object.new_colours = current_colours

        elif product.colour_set:
            current_colour_set = self.product_page.current_colour_set
            product_colour_set = product.colour_set

            if current_colour_set != product_colour_set:

                colour_messages = self.product_page.update_colour_set(product_colour_set)
                if len(colour_messages) == 0:
                    self.status_object.status = UPDATED
                else:
                    self.status_object.status = WARNING

                self.messages += colour_messages
                old_colour_set = current_colour_set
                current_colour_set = self.product_page.current_colour_set
                if old_colour_set != current_colour_set:
                    self.status_object.old_colours = old_colour_set
                    self.status_object.new_colours = current_colour_set