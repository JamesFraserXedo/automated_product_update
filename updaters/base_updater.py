import imghdr
import os
import struct
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

            colour_messages = self.product_form.update_colours(product_colours)
            if len(colour_messages) == 0:
                status = UPDATED
            else:
                status = WARNING

            messages += colour_messages
            old_colours = current_colours
            current_colours = self.product_form.get_current_colours()
            if old_colours != current_colours:
                messages.append("Updated colours from {} to {}".format(old_colours, current_colours))

        self.product_form.get_save_button().click()

        return StatusObject(status, messages)

    def handle_creation(self, product, messages):
        print(self.get_path_to_image(product.style))

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
                status = WARNING
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

    def get_path_to_image(self, code):
        base_dir = 'X:\Xedo Support\Bridal Designers Info\Mori Lee'

        preferred = None
        all = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.startswith(code):
                    all.append(os.path.join(root, file))
                    if not preferred and self.is_portrait(os.path.join(root, file)):
                        preferred = os.path.join(root, file)
        if not preferred and len(all) > 0:
            preferred = all[0]
        return preferred, all

    def is_portrait(self, fname):
        sizes = self.get_image_size(fname)
        return sizes[0] < sizes[1]

    def get_image_size(self, fname):
        '''Determine the image type of fhandle and return its size.
        from draco'''
        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            if imghdr.what(fname) == 'png':
                check = struct.unpack('>i', head[4:8])[0]
                if check != 0x0d0a1a0a:
                    return
                width, height = struct.unpack('>ii', head[16:24])
            elif imghdr.what(fname) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            elif imghdr.what(fname) == 'jpeg':
                try:
                    fhandle.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception:  # IGNORE:W0703
                    return
            else:
                return
            return width, height